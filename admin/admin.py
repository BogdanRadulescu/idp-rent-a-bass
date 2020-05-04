from sanic import Sanic, response, request
import mysql.connector as db
from time import sleep
from uuid import uuid4

app = Sanic('rentabAss')
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
    try:
        cursor.callproc(name, args)
        for r in cursor.stored_results():
            res.append(r.fetchall())
        cnx.commit()
    except:
        print('An error has occured while trying to execute procedure')
    return res

@app.route('/login', methods=['GET'])
def login(req: request.Request):
    username, password = req.args['username'][0], req.args['password'][0]
    if username != 'admin' or password != 'admin':
        return response.redirect('/')
    return response.redirect('/all')

@app.route('/add_user', methods=['GET'])
def add_user(req: request.Request):
    global cursor
    username, password, uid = req.args['username'][0], req.args['password'][0], uuid4().__str__()
    reset_connection()
    res = callprocedure('insert_user', [uid, username, password])
    return response.redirect('/all')

@app.route('/add_instrument', methods=['GET'])
def add_instrument(req: request.Request):
    global cursor
    typee, name, cond, fabrication_year, iid =\
        req.args['type'][0], req.args['name'][0], req.args['cond'][0], req.args['fabrication_year'][0], uuid4().__str__()
    reset_connection()
    res = callprocedure('insert_instrument', [iid, typee, name, cond, fabrication_year])
    return response.redirect('/all')

app.static('/', 'pages/login.html')
app.static('/all', 'pages/all.html')
app.static('/user', 'pages/user.html')
app.static('/instrument', 'pages/instrument.html')
app.run(host='0.0.0.0', port=8009)