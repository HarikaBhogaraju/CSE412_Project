import csv

import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="cse412", user='hbhogara', password='db123', host='127.0.0.1', port= '5432'
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
descriptions  = []
benefits = []
price = 0
with open('PLANTS_database.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row)
    print(f'Processed {line_count} lines.')
'''
cursor.execute(createShop)
print("Table created successfully")
conn.commit()
