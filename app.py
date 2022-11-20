import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
       database="cse412", user='hbhogara', password='db123', host='127.0.0.1', port= '5432'
    )
    return conn

def verify(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    getCount = ''' SELECT COUNT(*) FROM Customer
    WHERE Customer.email = %s AND Customer.password = %s '''
    row = [username,password]
    cur.execute(getCount,row)
    count = cur.fetchall()
    cur.close()
    conn.close()
    print(count[0][0])
    if(count[0][0] == 0):
        return False
    else:
        return True
#@app.route('/')
#def hello():
    #return '<h1>Plant Store</h1>'
def addCustomer(cname,eml,pwd,s_a):
    conn = get_db_connection()
    cur = conn.cursor()
    data = [cname,eml,pwd,s_a]
    insertCustomer = ''' INSERT INTO
    Customer(customer_name,email,password,shipping_address)
    VALUES(%s,%s,%s,%s) '''
    cur.execute(insertCustomer,data)
    conn.commit()

@app.route('/products')
def getProducts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Product WHERE product_id < 101 ORDER BY product_id;')
    prods = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('products.html', prods=prods)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/account/<uname>/<password>')
def account(uname,password):
    status = verify(uname,password)
    print(status)
    if(status):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Product WHERE product_id < 101 ORDER BY product_id;')
        prods = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('products.html', prods=prods)
    else:
        print("THERE ARE ERRORS")
        return render_template('error.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      unm = request.form['username']
      pwd = request.form['password']
      return redirect(url_for('account',uname = unm,password=pwd))
   else:
      unm = request.form['username']
      pwd = request.form['password']
      return redirect(url_for('account',uname = unm,password=pwd))

@app.route('/signup_post',methods = ['POST', 'GET'])
def signup_post():
   if request.method == 'POST':
      unm = request.form['username']
      pwd = request.form['password']
      nm = request.form['name']
      add = request.form['address']
      addCustomer(nm,unm,pwd,add)
      return redirect(url_for('account',uname = unm,password=pwd))
