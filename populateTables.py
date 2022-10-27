import csv
import random

#Formatting data
descriptions  = ["Alpine plant", "Desert terrain plant","Tropical plant", "Coastal terrain plant",
                "Coniferous Tree", "Deciduous Tree", "Shrub", "Floral plant", "Fruit plant", "Indoor plant"]
benefits = ["Therapeutic", "Decorative", "Fruity","Healing abilities"]
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
            data_row.append(row[0]) #code
            data_row.append(row[0+2]) #name
            data_row.append(random.choice(benefits)) #benefit
            data_row.append(random.choice(descriptions)) #description
            data_row.append(round(random.uniform(1.00,20.00),2))#price
            line_count += 1

            print(data_row)

            data.append(data_row)

    print(f'Processed {line_count} lines.')
