import sqlite3
conn=sqlite3.connect('./library.db')
cur=conn.cursor()
# cur.execute('drop table records')
# cur.execute('drop table books')
cur.execute('CREATE TABLE books(book_id INTEGER PRIMARY KEY autoincrement, books_name TEXT, author TEXT, copies INTEGER, image TEXT)')

cur.execute('CREATE TABLE records(records_id INTEGER PRIMARY KEY autoincrement, book_user_id INTEGER,borrow_user_id INTEGER, from_date TEXT, to_date TEXT, book_returned TEXT, constraint fk_RECORDS_ID foreign key(book_user_id) references books(book_id), constraint fk_USER_USER_ID foreign key(borrow_user_id) references register_and_login(user_id))')


print('table created')
conn.commit()
conn.close()