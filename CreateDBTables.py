import csv

import psycopg2

#establishing the connection
#Change X and Y to appropriate username and password
conn = psycopg2.connect(
   database="cse412", user='hbhogara', password='db123', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Shop
createShop = '''CREATE TABLE Shop(
store_id SERIAL PRIMARY KEY,
phone_number CHAR(10) NOT NULL,
store_address VARCHAR(100) NOT NULL
)'''

#Products
createProduct = '''CREATE TABLE Product(
product_id SERIAL PRIMARY KEY,
product_code VARCHAR(20) NOT NULL,
product_name TEXT NOT NULL,
benefits TEXT,
description TEXT,
price FLOAT
)'''

#Payment
createPayment = '''CREATE TABLE Payment(
payment_id SERIAL PRIMARY KEY,
payment_type CHAR(1) NOT NULL,
cardholder_name CHAR(30) NOT NULL,
amount FLOAT NOT NULL,
card_number INT NOT NULL,
cvv INT NOT NULL,
expiry_date DATE NOT NULL
)'''

#Items
createItems = '''CREATE TABLE Items(
item_id SERIAL PRIMARY KEY,
unit_price FLOAT NOT NULL,
quantity INT NOT NULL,
cart_id INT NOT NULL,
product_id INT REFERENCES Product(product_id) NOT NULL
)'''

#Shopping Cart
createCart = '''CREATE TABLE Cart(
cart_id INT NOT NULL,
customer_id INT REFERENCES Customer(customer_id) NOT NULL,
total_amount FLOAT NOT NULL,
item INT REFERENCES Items(item_id) NOT NULL
)'''

#Bill
createBill = '''CREATE TABLE Bill(
bill_id SERIAL PRIMARY KEY,
payment_id INT REFERENCES Payment(payment_id) NOT NULL,
customer_name CHAR(30) NOT NULL,
total_amount FLOAT NOT NULL,
item INT NOT NULL
)'''

#Wish List
createWishlist = '''CREATE TABLE Wishlist(
wishlist_id SERIAL PRIMARY KEY,
customer_id INT REFERENCES Customer(customer_id) NOT NULL,
list_name CHAR(50) NOT NULL,
product_id INT REFERENCES Product(product_id) NOT NULL
)'''

#Customers
createCustomer = '''CREATE TABLE Customer(
customer_id SERIAL PRIMARY KEY,
customer_name CHAR(30) NOT NULL,
email VARCHAR(100) NOT NULL,
password VARCHAR(50) NOT NULL,
shipping_address VARCHAR(100) NOT NULL

)'''


#Feedback
createFeedback = '''CREATE TABLE Feedback(
feedback_id SERIAL PRIMARY KEY,
comment VARCHAR(200) NOT NULL,
customer_id INT REFERENCES Customer(customer_id) NOT NULL
)'''


#cursor.execute(createShop)
#print("Shop Table created successfully")

cursor.execute(createProduct)
print("Products Table created successfully")

#cursor.execute(createCustomer)
#print("Customer Table created successfully")

#cursor.execute(createFeedback)
#print("Feedback Table created successfully")

cursor.execute(createItems)
print("Items Table created successfully")

cursor.execute(createCart)
print("Cart Table created successfully")

#cursor.execute(createPayment)
#print("Payment Table created successfully")

#cursor.execute(createBill)
#print("Bill Table created successfully")

cursor.execute(createWishlist)
print("Wishlist Table created successfully")

conn.commit()
