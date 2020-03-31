from uuid import uuid4
import mysql.connector as db
from time import sleep
from datetime import date

cursor = None
cnx = None

def reset_connection():
    global cursor, cnx
    while(True):
        try:
            if cnx is not None:
                cnx.commit()
                cursor.close()
                cnx.close()
                cursor = None
            cnx = db.connect(user='root', password='password', host='localhost', database='musicdb')
            break
        except:
            print('[server] Server cannot connect to sql server; retrying in 5 seconds')
            sleep(5)
    if cursor is None:
        cursor = cnx.cursor()

USER_1 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88100',
    "username": "KirkHammett",
    "password": "default",
}
USER_2 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88101',
    "username": "AngusMcFife",
    "password": "default",
}
USER_3 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88102',
    "username": "AttilaDorn",
    "password": "default",
}
USER_4 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88103',
    "username": "JoachimBroden",
    "password": "default",
}
USER_5 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88104',
    "username": "JamesHetfield",
    "password": "default",
}

BANK_1 = {
    "account_number": '23b89938-353b-11ea-978f-2e728ce88600',
    "account_secret": 'bank_secret',
    "balance": 5000
}

BANK_2 = {
    "account_number": '23b89938-353b-11ea-978f-2e728ce88601',
    "account_secret": 'bank_secret',
    "balance": 2500
}
BANK_3 = {
    "account_number": '23b89938-353b-11ea-978f-2e728ce88602',
    "account_secret": 'bank_secret',
    "balance": 3000
}
BANK_4 = {
    "account_number": '23b89938-353b-11ea-978f-2e728ce88603',
    "account_secret": 'bank_secret',
    "balance": 6000
}
BANK_5 = {
    "account_number": '23b89938-353b-11ea-978f-2e728ce88604',
    "account_secret": 'bank_secret',
    "balance": 7000
}

USER_1_INFORMATION = {
    "id": '23b89938-353b-11ea-978f-2e728ce88200',
    "userid": USER_1["id"],
    "firstName": "Kirk",
    "lastName": "Hammett",
    "account_number": BANK_1["account_number"],
    "address": "Dumbrava Minunata, Sector 7, Bucuresti",
    "date_of_birth": date(1975, 10, 5),
    "preferred_instrument": "guitar"
}

USER_2_INFORMATION = {
    "id": '23b89938-353b-11ea-978f-2e728ce88201',
    "userid": USER_2["id"],
    "firstName": "Angus",
    "lastName": "McFife",
    "account_number": BANK_2["account_number"],
    "address": "Aleea Mantuirii, Sector 8, Bucuresti",
    "date_of_birth": date(1970, 8, 3),
    "preferred_instrument": "piano"
}

USER_3_INFORMATION = {
    "id": '23b89938-353b-11ea-978f-2e728ce88202',
    "userid": USER_3["id"],
    "firstName": "Attila",
    "lastName": "Dorn",
    "account_number": BANK_3["account_number"],
    "address": "Bd. Dracula, Sector 12, Bucuresti",
    "date_of_birth": date(1980, 2, 7),
    "preferred_instrument": None
}

USER_4_INFORMATION = {
    "id": '23b89938-353b-11ea-978f-2e728ce88203',
    "userid": USER_4["id"],
    "firstName": "Joachim",
    "lastName": "Broden",
    "account_number": BANK_4["account_number"],
    "address": "Calea Hristos, Sector 10, Bucuresti",
    "date_of_birth": date(1981, 11, 20),
    "preferred_instrument": "drums"
}


USER_5_INFORMATION = {
    "id": '23b89938-353b-11ea-978f-2e728ce88204',
    "userid": USER_5["id"],
    "firstName": "James",
    "lastName": "Hetfield",
    "account_number": BANK_5["account_number"],
    "address": None,
    "date_of_birth": date(1970, 5, 18),
    "preferred_instrument": None
}

INSTR_1 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88300',
    "type": "strings",
    'name': 'guitar',
    'cond': 7,
    'fabrication_year': 2015
}
INSTR_2 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88301',
    "type": "strings",
    'name': 'violin',
    'cond': 5,
    'fabrication_year': 2013
}
INSTR_3 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88302',
    "type": 'percussion',
    'name': 'drums',
    'cond': 10,
    'fabrication_year': 2018
}
INSTR_4 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88303',
    "type": "percussion",
    'name': 'cymbal',
    'cond': 6,
    'fabrication_year': 2010
}
INSTR_5 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88304',
    "type": "brass",
    'name': 'trumpet',
    'cond': 9,
    'fabrication_year': 2016
}
INSTR_6 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88305',
    "type": "brass",
    'name': 'tuba',
    'cond': 8,
    'fabrication_year': 2017
}
INSTR_7 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88306',
    "type": "keyboard",
    'name': 'piano',
    'cond': 4,
    'fabrication_year': 1997
}
INSTR_8 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88307',
    "type": "keyboard",
    'name': 'organ',
    'cond': 7,
    'fabrication_year': 1985
}
INSTR_9 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88308',
    "type": "strings",
    'name': 'bass',
    'cond': 10,
    'fabrication_year': 2000
}
INSTR_10 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88309',
    "type": "strings",
    'name': 'ukulele',
    'cond': 9,
    'fabrication_year': 1965
}

VENDOR_1 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88400',
    'userid': USER_1['id'],
    'instrumentid': INSTR_1['id'],
    'nr_items': 5,
    'price_per_day': 25
}
VENDOR_2 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88401',
    'userid': USER_1['id'],
    'instrumentid': INSTR_2['id'],
    'nr_items': 3,
    'price_per_day': 20
}
VENDOR_3 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88402',
    'userid': USER_1['id'],
    'instrumentid': INSTR_3['id'],
    'nr_items': 7,
    'price_per_day': 50
}
VENDOR_4 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88403',
    'userid': USER_2['id'],
    'instrumentid': INSTR_4['id'],
    'nr_items': 3,
    'price_per_day': 30
}
VENDOR_5 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88404',
    'userid': USER_2['id'],
    'instrumentid': INSTR_5['id'],
    'nr_items': 1,
    'price_per_day': 20
}
VENDOR_6 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88405',
    'userid': USER_2['id'],
    'instrumentid': INSTR_6['id'],
    'nr_items': 2,
    'price_per_day': 10
}
VENDOR_7 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88406',
    'userid': USER_3['id'],
    'instrumentid': INSTR_7['id'],
    'nr_items': 3,
    'price_per_day': 35
}
VENDOR_8 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88407',
    'userid': USER_4['id'],
    'instrumentid': INSTR_8['id'],
    'nr_items': 1,
    'price_per_day': 20
}
VENDOR_9 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88408',
    'userid': USER_4['id'],
    'instrumentid': INSTR_8['id'],
    'nr_items': 7,
    'price_per_day': 5
}
VENDOR_10 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88409',
    'userid': USER_5['id'],
    'instrumentid': INSTR_10['id'],
    'nr_items': 1,
    'price_per_day': 10000
}
VENDOR_11 = {
    "id": '23b89938-353b-11ea-978f-2e728ce88410',
    'userid': USER_5['id'],
    'instrumentid': INSTR_1['id'],
    'nr_items': 2,
    'price_per_day': 250
}
TRANSACT_1 = {
    'id': '23b89938-353b-11ea-978f-2e728ce88500',
    'buyerid': USER_2['id'],
    'vendorid': VENDOR_1['id'],
    'duration': 10
}
TRANSACT_2 = {
    'id': '23b89938-353b-11ea-978f-2e728ce88501',
    'buyerid': USER_2['id'],
    'vendorid': VENDOR_8['id'],
    'duration': 5
}
users = [USER_1, USER_2, USER_3, USER_4, USER_5]
banks = [BANK_1, BANK_2, BANK_3, BANK_4, BANK_5]
users_info = [USER_1_INFORMATION, USER_2_INFORMATION, USER_3_INFORMATION, USER_4_INFORMATION, USER_5_INFORMATION]
instruments = [INSTR_1, INSTR_2, INSTR_3, INSTR_4, INSTR_5, INSTR_6, INSTR_7, INSTR_8, INSTR_9, INSTR_10]
vendors = [VENDOR_1, VENDOR_2, VENDOR_3, VENDOR_4, VENDOR_5, VENDOR_6, VENDOR_7, VENDOR_8, VENDOR_9, VENDOR_10, VENDOR_11]
transactions = [
    #TRANSACT_1,
    #TRANSACT_2
]
def insert_users():
    reset_connection()
    for user in users:
        cursor.callproc('insert_user', list(user.values()))
        cnx.commit()
    return

def insert_banks():
    reset_connection()
    for bank in banks:
        cursor.callproc('insert_bank', list(bank.values()))
        cnx.commit()
    return


def insert_user_info():
    reset_connection()
    for user_info in users_info:
        cursor.callproc('insert_user_info', list(user_info.values()))
        cnx.commit()
    return

def insert_instruments():
    reset_connection()
    for instrument in instruments:
        cursor.callproc('insert_instrument', list(instrument.values()))
        cnx.commit()
    return

def insert_vendors():
    reset_connection()
    for vendor in vendors:
        cursor.callproc('insert_vendor', list(vendor.values()))
        cnx.commit()
    return

def insert_transactions():
    reset_connection()
    for tr in transactions:
        cursor.callproc('insert_transaction', list(tr.values()))
        cnx.commit()
    return

insert_users()
insert_banks()
insert_user_info()
insert_instruments()
insert_vendors()
#insert_transactions()