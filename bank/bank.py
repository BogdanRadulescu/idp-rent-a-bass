import sys
import mysql.connector as db
from sanic import Sanic, response, request
from time import sleep
import json
from uuid import uuid4
from glob import glob
from simplecrypt import decrypt

app = Sanic('admin_rentabAss')
cursor = None
cnx = None
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

@app.route('/', methods=['POST'])
def authorize_transact(req: request.Request):
    data = req.json
    dd = decrypt(secret, bytes(data['secret'], 'utf-8', errors='surrogateescape')).decode('utf8')
    reset_connection()
    cursor.execute('select validate_secret(%s, %s)', (data['from'], dd))
    res = cursor.fetchone()
    if int(res[0]) != 1:
        return response.text('UNAUTH', status=400)
    
    reset_connection()
    cursor.execute('select get_money(%s, %s)', (data['from'], dd))
    res = cursor.fetchone()
    if int(res[0]) < data['sum']:
        return response.text('NOCASH', status=400)

    reset_connection()
    args = [data['from'], data['to'], data['sum']]
    cursor.callproc('move_money', args)
    cnx.commit()
    return response.text('OK')

@app.route('/ping')
def ping(req: request.Request):
    return response.text('IT WORKS')

@app.route('/wealth', methods=['POST'])
def balance(req: request.Request):
    data = req.json
    dd = decrypt(secret, bytes(data['secret'], 'utf-8', errors='surrogateescape')).decode('utf8')

    reset_connection()
    cursor.execute('select get_money(%s, %s)', (data['account_number'], dd))
    res = cursor.fetchone()
    return response.text(res[0])

app.run(host='0.0.0.0', port='8008')