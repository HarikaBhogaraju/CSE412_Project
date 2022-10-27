import csv
import random
import psycopg2

#establishing the connection
#Change X and Y to appropriate username and password
conn = psycopg2.connect(
   database="cse412", user='hbhogara', password='db123', host='127.0.0.1', port= '5432'
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
#Formatting data
descriptions  = ["Alpine", "Desert","Tropical", "Coastal",
                "Coniferous", "Deciduous", "Shrub", "Floral", "Fruit", "Indoor"]
benefits = ["Therapeutic", "Decorative", "Fruity","Healing"]
price = 0
data = []
with open('PLANTS_database.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data_row = []
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            row[2] = row[2].replace(" ","-")
            row[2] = row[2].replace("(","-")
            row[2] = row[2].replace(")","-")
            data_row.append(row[0]) #code
            data_row.append(row[0+2]) #name
            data_row.append(random.choice(benefits)) #benefit
            data_row.append(random.choice(descriptions)) #description
            data_row.append(str(round(random.uniform(1.00,20.00),2)))#price
            line_count += 1

            print(data_row)

            data.append(data_row)

    print(f'Processed {line_count} lines.')


for row in data:
    #insertProduct = "INSERT INTO Product (product_code,product_name,benefits,description,price) VALUES ("+ str(row[0]) + ","+ str(row[1]) + ","+ str(row[2]) + ","+ str(row[3]) + ","+ str(row[4]) + ")"
    insertProduct = ''' INSERT INTO
    Product(product_code,product_name,benefits,description,price)
    VALUES(%s,%s,%s,%s,%s) '''
    cursor.execute(insertProduct,row)
    conn.commit()
