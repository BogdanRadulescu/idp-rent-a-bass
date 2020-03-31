create database musicdb;
use musicdb;
create table users (
    id varchar(50),
    username varchar(50) not null,
    password text not NULL,
    UNIQUE (username),
    PRIMARY KEY (id)
);
create table bank (
    account_number varchar(50),
    account_secret varchar(50),
    account_balance INTEGER,
    PRIMARY KEY (account_number)
);
create table user_information (
    id varchar(50),
    userid varchar(50) not null,
    first_name text not null,
    last_name text not null,
    account_number varchar(50) not null,
    address text,
    date_of_birth date,
    preferred_instrument text,
    PRIMARY KEY (id),
    FOREIGN KEY (userid) REFERENCES users (id),
    FOREIGN KEY (account_number) REFERENCES bank (account_number)
);

create table instruments (
    id varchar(50),
    type text not null,
    name text not null,
    cond INTEGER,
    fabrication_year INTEGER,
    PRIMARY KEY (id)
);

create table vendors (
    id varchar(50),
    userid varchar(50) not null,
    instrumentid varchar(50) not null,
    nr_items INTEGER,
    price_per_day INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (userid) REFERENCES users (id),
    FOREIGN key (instrumentid) REFERENCES instruments (id)
);

create table transactions (
    id varchar(50),
    buyerid varchar(50) not null,
    vendorid varchar(50) not null,
    duration INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (buyerid) REFERENCES users (id)
);