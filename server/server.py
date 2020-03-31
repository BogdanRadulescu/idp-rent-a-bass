import sys
import mysql.connector as db
from sanic import Sanic, response, request
from time import sleep
import json
from uuid import uuid4
from glob import glob
import requests
from simplecrypt import encrypt

app = Sanic('rentabAss')
cursor = None
cnx = None
currentUser = None
currentProduct = None
secret = 's3cr3t_r3nt@b@$$'

def reset_connection():
    global cursor, cnx
    while(True):
        try:
            if cnx is not None:
                cnx.commit()
                cursor.close()
                cnx.close()
                cursor = None
            cnx = db.connect(user='root', password='password', host='database', database='musicdb')
            break
        except:
            print('[server] Server cannot connect to sql server; retrying in 5 seconds')
            sleep(5)
    if cursor is None:
        cursor = cnx.cursor()

def callprocedure(name: str, args):
    res = []
    reset_connection()
    cursor.callproc(name, args)
    for r in cursor.stored_results():
        res.append(r.fetchall())
    return res

@app.route('wealth', methods=['GET'])
def wealth(req: request.Request):
    secret_text = encrypt(secret, currentUser["secret"]).decode(errors='surrogateescape')
    data = {
        'account_number': currentUser['account_number'],
        'secret': secret_text
    }
    res = requests.post('http://bank:8008/wealth', json=data)
    return response.text(res.text)


@app.route('/login', methods=['GET'])
def login(req: request.Request):
    reset_connection()
    username, password, secret = req.args['username'][0], req.args['password'][0], req.args['secret'][0]
    cursor.execute('select attempt_login(%s, %s, %s)', (username, password, secret))
    res = cursor.fetchone()
    if res[0] == "":
        return response.redirect('/')
    reset_connection()
    cursor.callproc('get_user_info', [res[0]])
    for r in cursor.stored_results():
        re = r.fetchall()[0]
        global currentUser
        currentUser = {
            "id": re[1],
            "first_name": re[2],
            "last_name": re[3],
            "account_number": re[4],
            "address": re[5],
            "date_of_birth": re[6],
            "preferred_instrument": re[7],
            "secret": secret
        }
    return response.redirect('/loggedin')

@app.route('/test', methods=['GET'])
def test(req: request.Request):
    s = f'{glob("./*")}{glob("./*/*")}'
    return response.text(s)

@app.route('/buyproduct', methods=["POST"])
def buyproduct(req: request.Request):
    global currentProduct
    res = json.loads(req.body)
    currentProduct = res
    currentProduct["nr_available"] = int(currentProduct["nr_available"])
    return response.text('OK')

@app.route('/buyform', methods=["POST"])
def buyform(req: request.Request):
    global currentProduct
    if currentProduct is None:
        return response.text('No product selected')
    return response.json(currentProduct)

@app.route('/reserve-instrument', methods=["GET"])
def reserve_instrument(req: request.Request):
    reset_connection()
    cursor.callproc('get_user_info_by_uname', [currentProduct['vendor']])
    vendor_user = None
    for res in cursor.stored_results():
        vendor_user = res.fetchall()
    cost = int(req.args["daystorent"][0]) * int(currentProduct["price_per_day"])
    auth_data = {
        "to": vendor_user[0][4],
        "from": currentUser["account_number"],
        "sum": cost,
        "secret": encrypt(secret, currentUser["secret"]).decode(errors='surrogateescape')
    }
    authorized = requests.post('http://bank:8008/', json=auth_data)
    if authorized.status_code == 400:
        if authorized.text == 'NOCASH':
            return response.text(f'You do not have enough money, you need {cost}', status=400)
        if authorized.text == 'UNAUTH':
            return response.text(f'User secret does not match server side', status=400)
    reset_connection()
    args = [uuid4().__str__(), currentUser["id"], currentProduct["id"], int(req.args["daystorent"][0])]
    cursor.callproc("insert_transaction", args)
    currentProduct['nr_available'] -= int(req.args["daystorent"][0])
    cnx.commit()
    return response.redirect('/profile')

@app.route('get-rented-instruments', methods=['GET'])
def get_rented_instruments(req: request.Request):
    reset_connection()
    cursor.callproc('get_rented_instruments', [currentUser['id']])
    for res in cursor.stored_results():
        body = [{"buyer": buyer, "nr": nr} for buyer, nr in res.fetchall()]
        return response.json(body)

@app.route('get-balance', methods=['GET'])
def get_rented_instruments(req: request.Request):
    reset_connection()
    cursor.callproc('get_balance', [currentUser['id']])
    for res in cursor.stored_results():
        data = res.fetchall()
        body = [{"uname": uname, "name": name, "type": typee, "price_per_day": price_per_day, "nr": int(nr)} for uname, name, typee, price_per_day, nr in data]
        return response.json(body)

@app.route('/mainpage', methods=['GET'])
def mainpage(req: request.Request):
    reset_connection()
    global currentUser
    if currentUser is None:
        return response.redirect('/')
    cursor.callproc('get_all_instruments', [currentUser["id"]])
    for res in cursor.stored_results():
        body = [{"id": id, "vendor": username, "type": type, "name": name,
        "cond": cond, "fabrication_year": fabrication_year, "nr_items": nr_items, "price_per_day": price_per_day} for
        id, username, type, name, cond, fabrication_year, nr_items, price_per_day
        in res.fetchall()]
        return response.json(body)

@app.route('/users', methods=['GET'])
def get_users(req):
    global cursor
    reset_connection()
    cursor.callproc('get_users')
    for res in cursor.stored_results():
        body = [{"id": id, "username": username} for id, username in res.fetchall()]
        return response.json(body)

@app.route('/user-information', methods=['GET'])
def get_user_info(req):
    global cursor
    reset_connection()
    cursor.callproc('get_users')
    for res in cursor.stored_results():
        body = [{"id": id, "username": username} for id, username in res.fetchall()]
        return response.json(body)


app.static('/', 'pages/login.html')
app.static('/loggedin', 'pages/main.html')
app.static('/buyform', 'pages/buyform.html')
app.static('/profile', 'pages/profile.html')
app.run(host='0.0.0.0', port=8000)

