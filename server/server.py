import sys
import mysql.connector as db
from sanic import Sanic, response, request
from time import sleep
import json
from uuid import uuid4
from glob import glob
#from pages.mainpage import *

app = Sanic('rentabAss')
cursor = None
cnx = None
currentUser = None
currentProduct = None


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

@app.route('/login', methods=['GET'])
def login(req: request.Request):
    reset_connection()
    username, password = req.args['username'][0], req.args['password'][0]
    cursor.execute('select attempt_login(%s, %s)', (username, password))
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
            "credit": re[4],
            "address": re[5],
            "date_of_birth": re[6],
            "preferred_instrument": re[7]
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
    cost = int(req.args["daystorent"][0]) * int(currentProduct["price_per_day"])
    if currentUser["credit"] < cost:
        return response.text(f'You do not have enough money: You have {currentUser["credit"]} and you need {cost}')
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

