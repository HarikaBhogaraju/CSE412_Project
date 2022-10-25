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
