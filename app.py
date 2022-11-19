import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
       database="cse412", user='hbhogara', password='db123', host='127.0.0.1', port= '5432'
    )
    return conn


#@app.route('/')
#def hello():
    #return '<h1>Plant Store</h1>'

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

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
