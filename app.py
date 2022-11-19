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

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Product WHERE product_id < 101 ORDER BY product_id;')
    prods = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', prods=prods)
