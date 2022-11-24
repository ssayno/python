import sqlite3
import csv
import time

connect = sqlite3.connect('sku_query.db')
cursor = connect.cursor()
category = 'halloween'
create_category_table = f'''\
create table if not exists categories(
hash_id int primary key,
category_name text
)
'''
create_sku_table = f'''\
create table if not exists skus(
parent_hash_id int,
sku text primary key,
url text
)
'''
cursor.execute(create_category_table)
cursor.execute(create_sku_table)
cursor.execute('insert into categories values (?, ?)', (hash(category), category))
connect.commit()
unique = []
with open('halloween.csv', 'r', encoding='U8') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)
    for row in csv_reader:
        try:
            unique.append(row[0])
        except IndexError:
            continue
        need = (hash(category), row[0], row[1])
        try:
            cursor.execute('insert into skus values (?, ?, ?)', need)
            connect.commit()
        except Exception as e:
            connect.rollback()
cursor.close()
connect.close()
print(len(unique), len(set(unique)))
with open('a', 'w+', encoding='U8') as f:
    f.write('\n'.join(unique))
