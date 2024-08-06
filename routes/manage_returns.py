import sqlite3 as sql

from flask import render_template, session



def manage_returns_():
    if not session.get("authenticated", False):
        return render_template("login.html", error_message="You haven't logged in")

    database_connection = None
    user_id = session["user_id"]
    from_date=''

    try:
        with sql.connect("library.db") as database_connection:
            cursor = database_connection.cursor()
            cursor.execute(
                'SELECT book_user_id FROM records WHERE book_returned="No" AND borrow_user_id=?',
                [user_id],
            )
            unreturned_books = cursor.fetchall()
            book_details_list = []
            for record in unreturned_books:
                for book_id in record:
                    cursor.execute(
                        "SELECT image, book_id, author, books_name FROM books WHERE book_id=?",
                        [book_id],
                    )
                    book_details = cursor.fetchall()
                    for detail in book_details:
                        book_details_list.append(detail)
                    print(book_details_list)

                    cursor.execute('Select to_date FROM records WHERE book_user_id=?',[book_id])
                    from_date=cursor.fetchall()
                    print(from_date)
                    print(from_date[-1])

    except Exception as e:
        if database_connection:
            database_connection.rollback()
    finally:
        if database_connection:
            database_connection.close()
        return render_template("return.html", book_details_list=book_details_list,from_date=from_date)
