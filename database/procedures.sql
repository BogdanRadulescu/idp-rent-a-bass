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

CREATE PROCEDURE get_user_info_by_uname(IN username varchar(50))
BEGIN
    select * from user_information ui, users u WHERE
    ui.userid=u.id AND u.username=username;
END //

CREATE FUNCTION validate_secret(
    an varchar(50),
    secret varchar(50)
) RETURNS INTEGER BEGIN
    DECLARE valid INTEGER;
    SET valid = 0;
    SELECT count(*) INTO valid from bank
    WHERE account_number = an AND account_secret = secret;
    return valid;
END//

CREATE FUNCTION get_money(
    an varchar(50),
    secret varchar(50)
) RETURNS INTEGER BEGIN
    DECLARE balance INTEGER;
    SELECT account_balance INTO balance from bank
    WHERE account_number = an AND account_secret = secret;
    return balance;
END//

CREATE PROCEDURE move_money(
    IN from_acc varchar(50),
    IN to_acc varchar(50),
    IN amount INTEGER
) BEGIN
    UPDATE bank set account_balance = account_balance - amount
    WHERE account_number = from_acc;
    UPDATE bank set account_balance = account_balance + amount
    WHERE account_number = to_acc;
END //

CREATE FUNCTION attempt_login(
    user text,
    pwd text,
    secret text
) RETURNS TEXT
BEGIN
    DECLARE res TEXT;
    set res = "";
    SELECT u.id INTO res FROM users u, bank b, user_information ui WHERE u.username=user AND u.password=pwd
        AND ui.userid=u.id AND ui.account_number=b.account_number AND b.account_secret=secret;
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
    IN account_number varchar(50),
    IN address text,
    IN date_of_birth DATE,
    IN preferred_instrument text
    ) BEGIN
    INSERT INTO user_information (id, userid, first_name, last_name, account_number, address, date_of_birth, preferred_instrument) values 
    (id, userid, first_name, last_name, account_number, address, date_of_birth, preferred_instrument);
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

CREATE PROCEDURE insert_bank(
    IN account_number varchar(50),
    IN account_secret varchar(50),
    IN account_balance INTEGER
) BEGIN
    INSERT INTO bank (account_number, account_secret, account_balance) VALUES
    (account_number, account_secret, account_balance);
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
UPDATE vendors SET nr_items=nr-1 WHERE id=NEW.vendorid;
END//

CREATE PROCEDURE get_balance(
    IN id varchar(50)
) BEGIN
    SELECT u.username as uname, i.name as name, i.type as type, v.price_per_day as price_per_day, sum(t.duration) as nr
    FROM instruments i, vendors v, transactions t, users u
    WHERE i.id = v.instrumentid AND v.id = t.vendorid AND id = v.userid AND u.id=t.buyerid
    GROUP BY uname, name, type, v.price_per_day
    UNION
    SELECT u.username as uname, i.name as name, i.type as type, -v.price_per_day as price_per_day, sum(t.duration) as nr
    FROM instruments i, vendors v, transactions t, users u
    WHERE id = t.buyerid AND t.vendorid = v.id AND v.instrumentid = i.id AND u.id=v.userid
    GROUP BY uname, name, type, v.price_per_day;
END//

SELECT u.username as uname, i.name as name, i.type as type, -v.price_per_day as price_per_day, sum(t.duration) as nr
    FROM instruments i, vendors v, transactions t, users u
    WHERE t.buyerid="23b89938-353b-11ea-978f-2e728ce88100" AND t.vendorid = v.id AND v.instrumentid = i.id AND u.id=v.userid
    GROUP BY uname, name, type, v.price_per_day;

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
    FROM vendors v, instruments i, users u
    WHERE v.instrumentid = i.id AND v.userid = u.id AND id <> u.id AND v.nr_items > 0
    ORDER BY i.type;
END//

DELIMITER ;
