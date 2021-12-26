import sqlite3
conn=sqlite3.connect('library.db')
cur=conn.cursor()
cur.execute('CREATE TABLE register_and_login(user_id INTEGER PRIMARY KEY autoincrement, Username TEXT, password TEXT, email TEXT, role TEXT)')
# cur.execute('drop table register_and_login')
conn.commit()
conn.close()