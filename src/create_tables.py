import sqlite3

connection = sqlite3.connect('data.db')
cursor= connection.cursor()

create_user_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY , username text, password txt)"
create_item_table_query = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY ,  name text, price int )"
cursor.execute(create_item_table_query)
cursor.execute(create_user_table_query)
connection.commit()
connection.close()
