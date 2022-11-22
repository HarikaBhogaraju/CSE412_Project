import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
num = 0

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

def getCID(username):
    conn = get_db_connection()
    cur = conn.cursor()
    getcid = ''' SELECT customer_id FROM Customer
    WHERE Customer.email = %s'''
    row = [username]
    cur.execute(getcid,row)
    cid = cur.fetchall()
    cur.close()
    conn.close()
    #print(cid[0][0])
    return cid

def getCartID(custid):
    cartID = 1

    conn = get_db_connection()
    cur = conn.cursor()

    getcidCount = ''' SELECT COUNT(*) FROM Cart
    WHERE customer_id = %s;'''
    row = [custid]
    cur.execute(getcidCount,row)
    cidCount = cur.fetchall()

    #check COUNT
    if(cidCount[0][0] == 0):
        #create cart
        getcidCount = ''' SELECT COUNT(*) FROM Cart;'''
        cur.execute(getcidCount)
        cidCount = cur.fetchall()
        cartID = cidCount
        print(cartID)
        return int(cartID[0][0])+1
    else:
        #add with existing cart ID
        getCrtID = ''' SELECT cart_id FROM Cart
        WHERE Cart.customer_id = %s;'''
        cur.execute(getCrtID,row)
        x = cur.fetchall()
        cartID = x[0][0]
        return cartID

    cur.close()
    conn.close()

def totalAmountCalc(cartID):
    conn = get_db_connection()
    cur = conn.cursor()
    getcidCount = ''' SELECT SUM(unit_price*quantity) FROM Items
    WHERE Items.cart_id = %s GROUP BY item_id'''
    row = [cartID]
    cur.execute(getcidCount,row)
    x = cur.fetchall()
    itemSum = x
    print("SUM = ",itemSum)
    return itemSum

def allItems(cartID):
    conn = get_db_connection()
    cur = conn.cursor()
    getcidCount = ''' SELECT item_id FROM Items
    WHERE Items.cart_id = %s'''
    row = [cartID]
    cur.execute(getcidCount,row)
    x = cur.fetchall()
    items = x
    print("last = ",items)
    return items

def totalAmountItems(cartID):
    conn = get_db_connection()
    cur = conn.cursor()
    getCost = ''' SELECT SUM(unit_price*quantity) FROM Items
    WHERE Items.cart_id = %s GROUP BY Items.cart_id'''

    row = [cartID]
    cur.execute(getCost,row)
    x = cur.fetchall()
    print("total sum = ",x)
    return x[0][0]

@app.route('/products/<uname>')
def getProducts(uname):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Product WHERE product_id < 101 ORDER BY product_id;')
    prods = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('products.html', prods=prods, username=uname)

def addtoWishlist():
    return "Added"

def removeFromWishlist():
    return "Removed"

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
        return render_template('products.html', prods=prods, username=uname)
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

@app.route('/cart_processing', methods=['POST','GET'])
def cart_processing():
    conn = get_db_connection()
    cur = conn.cursor()
    insertItem = ''' INSERT INTO Items(unit_price, quantity, cart_id, product_id) VALUES(%s,%s,%s,%s)'''

    if request.method == 'POST':
        pid = request.form['prod_id']
        prc = request.form['prod_price']
        q = request.form['quantity']
        unm = request.form['username']
        cust_id = getCID(unm)
        print("Cust ID = ", cust_id[0][0])
        s = cust_id[0][0]
        crt_id = getCartID(s)
        #create item
        data = [prc,q,crt_id,pid]
        cur.execute(insertItem,data)
        conn.commit()
        updateCart = ''' UPDATE Cart SET customer_id = %s, total_amount = %s, item = %s  WHERE cart_id = %s;'''

        items = allItems(crt_id)
        itemCount = items[len(items)-1][0]
        row = [crt_id, cust_id[0][0],round(float(prc)*int(q),2),itemCount]
        cur.execute(updateCart,row)
        conn.commit()

#Total cart cost
        sumQ = totalAmountItems(crt_id)
        sum = sumQ
        sum = round(sum,2)
        return redirect(url_for('cart',totalSum = sum,uname=unm))
    else:
        return "Failed to add to cart"

@app.route('/cart/<totalSum>/<uname>')
def cart(totalSum,uname):
    sum = totalSum
    return render_template('cart.html',totalSum=sum,uname=uname)

@app.route('/payment/<totalSum>/<uname>')
def payment(totalSum,uname):
    sum = totalSum
    return render_template('payment.html',totalSum=sum,uname=uname)

@app.route('/payment_processing', methods=['POST','GET'])
def payment_processing():
    conn = get_db_connection()
    cur = conn.cursor()
    insertPayment = ''' INSERT INTO Payment(payment_type,cardholder_name,amount,card_number,cvv,expiry_date) VALUES(%s,%s,%s,%s,%s,%s)'''
    if request.method == 'POST':
        card_name = request.form['cname']
        card_amt = request.form['cart_sum']
        card_no = request.form['cno']
        type = request.form['ctype']
        uname = request.form['uname']

        card_type = ''
        if(type == "Credit" or type == "credit"):
            card_type = 'C'
        else:
            card_type = 'D'

        card_cvv = request.form['cvv']
        card_exp_date = request.form['exp_date']
        row = [card_type,card_name,card_amt,card_no,card_cvv,card_exp_date]
        cur.execute(insertPayment,row)
        conn.commit()
        return redirect(url_for('bill_processing',card_amt = card_amt,uname=uname))
    else:
        card_name = request.form['cname']
        card_amt = request.form['cart_sum']
        card_no = request.form['cno']
        type = request.form['ctype']
        uname = request.form['uname']

        card_type = ''
        if(type == "Credit" or type == "credit"):
            card_type = 'C'
        else:
            card_type = 'D'

        card_cvv = request.form['cvv']
        card_exp_date = request.form['exp_date']
        row = [card_type,card_name,card_amt,card_no,card_cvv,card_exp_date]
        cur.execute(insertPayment,row)
        conn.commit()
        return redirect(url_for('bill_processing',card_amt = card_amt,uname=uname))

@app.route('/bill_processing/<card_amt>/<uname>')
def bill_processing(card_amt,uname):
    conn = get_db_connection()
    cur = conn.cursor()
    getItemNames = ''' SELECT product_name FROM Product, Items WHERE Product.product_id = Items.product_id AND Items.item_id = %s'''
    getItemCosts = ''' SELECT (unit_price*quantity) FROM Product, Items WHERE Product.product_id = Items.product_id AND Items.item_id = %s'''
    #get customer id from username
    cust_id = getCID(uname)
    print("Cust ID = ", cust_id[0][0])
    s = cust_id[0][0]

    #get card id from customer id
    crt_id = getCartID(s)

    #get all items from
    itemsNoTemp = allItems(crt_id)
    itemsNoList = []
    for i in range(len(itemsNoTemp)): #get each item ID
        itemsNoList.append(itemsNoTemp[i][0])

    itemID = 0

    itemsNameList = []
    for i in range(len(itemsNoList)):
        itemID = itemsNoList[i]
        row = [itemID]
        cur.execute(getItemNames,row)
        name = cur.fetchall()
        itemsNameList.append(name[0][0])

    itemsTotalCostList = []
    for i in range(len(itemsNoList)):
        itemID = itemsNoList[i]
        row = [itemID]
        cur.execute(getItemCosts,row)
        cost = cur.fetchall()
        itemsTotalCostList.append(round(cost[0][0],2))

    itemsList = []
    for i in range(len(itemsNoList)):
        item = [itemsNameList[i],itemsTotalCostList[i]]
        itemsList.append(item)

    #delete all cart and items

    return render_template('bill.html',Items=itemsList,uname=uname,totalSum=card_amt)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

def addFeedback(comment,customer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    data = [comment,customer_id[0][0]]
    insertFeedback = ''' INSERT INTO
    Feedback(comment,customer_id)
    VALUES(%s,%s)'''
    cur.execute(insertFeedback,data)
    conn.commit()

@app.route('/feedback_post',methods = ['GET', 'POST'])
def feedback_post():
   if request.method == 'POST':
       name = request.form['name']
       email = request.form['email']
       feedback = request.form['feedback']

       if (name=="" or feedback==""):
           return render_template('feedback.html', message = 'Please fill in the fields')

       addFeedback(feedback,getCID(email))
       return render_template('feedback_submitted.html')
   else:
       name = request.form['name']
       email = request.form['email']
       feedback = request.form['feedback']

       if (name=="" or feedback==""):
           return render_template('feedback.html', message = 'Please fill in the fields')

       addFeedback(feedback,getCID(email))
       return render_template('feedback_submitted.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

wishlist = []

@app.route('/wishlist_post', methods=['POST','GET'])
def wishlist_post():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        pid = request.form['prod_id']
        global wishlist
        wishlist.append(pid)
        
        #cur.execute(updateCart,row)
        #conn.commit()
    
    return redirect(url_for('wishlist',wishlist=wishlist))   

@app.route('/delete_wishItem/<pid>')
def delete_wishItem(pid):
    itemID = pid
    global wishlist
    wishlist.remove(pid)

    return redirect(url_for('wishlist',pid=itemID))
