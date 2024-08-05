import sqlite3 as sql
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, session

def borrow_(books):
    if session.get("authenticated", False) == False:
        return render_template("login.html", error_message="You haven't logged in")
    session["books"] = books

    author=''
    image=''

    try:
        with sql.connect("library.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT author,image FROM books WHERE books_name=?",
                [books],
            )
            all_content = cursor.fetchall()
            author=all_content[0][0]
            image=all_content[0][1]

            cursor.execute('SELECT books_name,author,image FROM books')
            extra_books = cursor.fetchall()

    except Exception as e:
        connection.rollback()
    finally:
        return render_template("booking_page.html", books=books, author=author, image=image, extra_books=extra_books)
