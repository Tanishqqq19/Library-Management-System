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
            print(111)
            cursor.execute(
                'SELECT book_user_id, to_date FROM records WHERE book_returned="No" AND borrow_user_id=?',
                [user_id],
            )
            print(2)
            unreturned_books = cursor.fetchall()
            book_details_list = []
            for record in unreturned_books:
                print(record)
                print('----')
                # for book_id in record:
                cursor.execute(
                    "SELECT image, book_id, author, books_name FROM books WHERE book_id=?",
                    [record[0]],
                )
                detail_add=[]
                book_details = cursor.fetchall()
                for detail in book_details:
                    for i in detail:
                        detail_add.append(i)
                    detail_add.append(record[1])
                    print(detail_add)
                    book_details_list.append(detail_add)
                    # print(book_details_list)

                    # cursor.execute('Select to_date FROM records WHERE book_user_id=?',[book_id])
                    # from_date=cursor.fetchall()
                    # print(from_date)
                    # print(from_date[-1])

    except Exception as e:
        if database_connection:
            database_connection.rollback()
    finally:
        if database_connection:
            database_connection.close()
        return render_template("return.html", book_details_list=book_details_list,from_date=from_date)
