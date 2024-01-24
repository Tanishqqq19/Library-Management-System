import sqlite3
conn=sqlite3.connect('../library.db')
cur=conn.cursor()
cur.execute('drop table records')
cur.execute('drop table books')
cur.execute('''
    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        books_name TEXT,
        author TEXT,
        copies INTEGER,
        image TEXT
    )
''')

cur.execute('''
    CREATE TABLE records(
        records_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        book_user_id INTEGER,
        book_user_name TEXT,
        borrow_user_id INTEGER, 
        borrow_user_name TEXT,
        from_date TEXT, 
        to_date TEXT, 
        book_returned TEXT, 
        FOREIGN KEY(book_user_id) REFERENCES books(book_id),
        FOREIGN KEY(borrow_user_id) REFERENCES users(user_id),
        FOREIGN KEY(borrow_user_name) REFERENCES register_and_login(Username)
    )
''')

#database_cursor.execute('INSERT INTO records(book_user_id, borrow_user_name, borrow_user_id, book_name,from_date, to_date, book_returned) VALUES (?, ?, ?, ?, ?, ?, ?)', (book_id, session_borrow_user_name,  session_user_id, session_books, current_date, target_date, "No"))

print('table created')
conn.commit()
conn.close()
