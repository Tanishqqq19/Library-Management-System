import sqlite3 as sql
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, session


def borrow_duration_():
    if request.method=="POST":
        session_books = session["books"]
        session_user_id = session["user_id"]
        session_borrow_user_name = session["Username"]

        time=request.form.get('weeks')
        print(time)

        if time==None:
            time=0



        database_connection = None

        try:
            with sql.connect("library.db") as database_connection:
                database_cursor = database_connection.cursor()
                database_cursor.execute(
                    "SELECT copies, book_id FROM books WHERE books_name = ?",
                    [session_books],
                )
                book_records = database_cursor.fetchall()
                for record in book_records:
                    book_copies = record[0]
                    book_id = record[1]

                current_date = date.today()
                target_date = current_date + timedelta(days=int(time))
                # target_date = current_date + timedelta(days=1)
                database_cursor.execute(
                    "SELECT from_date, to_date FROM records WHERE book_returned = 'No' AND book_user_id = ?",
                    [book_id],
                )
                borrow_dates = database_cursor.fetchall()
                for date_record in borrow_dates:
                    if (len(borrow_dates) - 1) >= book_copies:
                        return render_template(
                            "one_week.html", ref="Sorry you cannot borrow"
                        )
                    if str(current_date) > date_record[0]:
                        database_cursor.execute(
                            "INSERT INTO records(book_user_id, book_user_name, borrow_user_id, borrow_user_name,from_date, to_date, book_returned) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (
                                book_id,
                                session_books,
                                session_user_id,
                                session_borrow_user_name,
                                current_date,
                                target_date,
                                "No",
                            ),
                        )
                        return render_template("one_week.html", ref="borrowed")

        except Exception as e:
            if database_connection:
                database_connection.rollback()
        return render_template("one_week.html", ref="doesn't work")
    
    else:
        return render_template("booking_page.html")