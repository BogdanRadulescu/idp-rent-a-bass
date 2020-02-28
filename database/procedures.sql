use musicdb;

DELIMITER //
CREATE PROCEDURE get_users()
BEGIN
    SELECT id, username from users;
END //

CREATE PROCEDURE get_user_info(IN id varchar(50))
BEGIN
    select * from user_information where userid=id;
END //

CREATE FUNCTION attempt_login(
    user text,
    pwd text
) RETURNS TEXT
BEGIN
    DECLARE res TEXT;
    set res = "";
    SELECT id INTO res FROM users WHERE username=user AND password=pwd;
    return res;
END //

CREATE PROCEDURE insert_user(IN id varchar(50), IN username text, IN password text)
BEGIN
    INSERT INTO users (id, username, password) values (id, username, password);
END //

CREATE PROCEDURE insert_user_info(
    IN id varchar(50),
    IN userid varchar(50),
    IN first_name text,
    IN last_name text,
    IN credit INTEGER,
    IN address text,
    IN date_of_birth DATE,
    IN preferred_instrument text
    ) BEGIN
    INSERT INTO user_information (id, userid, first_name, last_name, credit, address, date_of_birth, preferred_instrument) values 
    (id, userid, first_name, last_name, credit, address, date_of_birth, preferred_instrument);
END //

CREATE PROCEDURE insert_instrument(
    IN id varchar(50),
    IN type text,
    IN name text,
    IN cond INTEGER,
    IN fabrication_year INTEGER
) BEGIN
    INSERT INTO instruments (id, type, name, cond, fabrication_year) VALUES
    (id, type, name, cond, fabrication_year);
END//

CREATE PROCEDURE insert_vendor(
    IN id varchar(50),
    IN userid varchar(50),
    IN instrumentid varchar(50),
    IN nr_items INTEGER,
    IN price_per_day INTEGER
) BEGIN
    INSERT INTO vendors (id, userid, instrumentid, nr_items, price_per_day) VALUES
    (id, userid, instrumentid, nr_items, price_per_day);
END//

CREATE PROCEDURE insert_transaction(
    IN id varchar(50),
    IN buyerid varchar(50),
    IN vendorid text,
    IN duration INTEGER
) BEGIN
    INSERT INTO transactions (id, buyerid, vendorid, duration) VALUES
    (id, buyerid, vendorid, duration);
END//

CREATE TRIGGER dec_vendor BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
DECLARE nr INTEGER;
SELECT nr_items INTO nr FROM vendors WHERE id=NEW.vendorid;
IF nr = 1 THEN
    DELETE FROM vendors WHERE id=NEW.vendorid;
ELSE
    UPDATE vendors SET nr_items=nr-1 WHERE id=NEW.vendorid;
END IF;
END//

CREATE PROCEDURE get_balance(
    IN id varchar(50)
) BEGIN
    SELECT u.username as uname, i.name as name, i.type as type, v.price_per_day as price_per_day, sum(t.duration) as nr
    FROM instruments i, vendors v, transactions t, users u
    WHERE i.id = v.instrumentid AND v.id = t.vendorid AND id = v.userid AND u.id=t.buyerid
    GROUP BY uname, name, type, price_per_day
    UNION
    SELECT u.username as uname, i.name as name, i.type as type, -v.price_per_day as price_per_day, sum(t.duration) as nr
    FROM instruments i, vendors v, transactions t, users u
    WHERE id = t.buyerid AND t.vendorid = v.id AND v.instrumentid = i.id AND u.id=v.userid
    GROUP BY uname, name, type, price_per_day;
END//

CREATE PROCEDURE get_rented_instruments(
    IN id varchar(50)
) BEGIN
    SELECT u.username as buyer, count(t.id) as nr FROM
    users u, transactions t, vendors v
    WHERE v.userid=id AND t.buyerid=u.id and t.vendorid=v.id
    GROUP BY u.username;
END//

CREATE PROCEDURE get_all_instruments(IN id varchar(50))
BEGIN
    SELECT v.id, u.username, i.type, i.name, i.cond, i.fabrication_year, v.nr_items, v.price_per_day
    FROM vendors v, instruments i, users u WHERE v.instrumentid = i.id AND v.userid = u.id AND id <> u.id
    ORDER BY i.type;
END//

DELIMITER ;
