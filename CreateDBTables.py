import csv

import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="cse412", user='ENTER YOUR POSTGRES USERNAME', password='ENTER YOUR POSTGRES PASSWORD(if applicable)', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Shop
createShop = '''CREATE TABLE Shop(
store_id INT NOT NULL PRIMARY KEY,
phone_number CHAR(10) NOT NULL,
store_address VARCHAR(100) NOT NULL
)'''
#Bill
createBill = '''CREATE TABLE Bill(

)'''
#Payment
createPayment = '''CREATE TABLE Payment(

)'''
#Wish List
createWishlist = '''CREATE TABLE Wishlist(

)'''
#Customers
createCustomer = '''CREATE TABLE Customer(

)'''
#Shopping Cart
create Cart = '''CREATE TABLE Cart(

)'''
#Items
createItems = '''CREATE TABLE Items(

)'''
#Feedback
createFeedback = '''CREATE TABLE Feedback(

)'''
#Products
createProduct = '''CREATE TABLE Product(

)'''

'''

'''
cursor.execute(createShop)
print("Table created successfully")
conn.commit()
