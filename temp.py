import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# create_table = "CREATE TABLE users (id int, username text, password text)"
#
# cursor.execute(create_table)

users = [
    (2, 'n', 'Bb123'),
    (3, 'f', 'Bb123')]


insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.executemany(insert_query, users)
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)
#cursor.execute(select_query)
connection.commit()
connection.close()