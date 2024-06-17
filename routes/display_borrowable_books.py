import sqlite3 as sql

from flask import render_template, session


def init_app(app):
    @app.route("/display_borrowable_books")
    def display_borrowable_books():
        if not session.get("authenticated", False):
            return render_template("login.html", error_message="You haven't logged in")

        connection = None
        available_book_ids = []
        book_names = []
        book_full_details = []

        try:
            with sql.connect("library.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT book_id, copies FROM books")
                books_and_copies = cursor.fetchall()

                for book_id, copies in books_and_copies:
                    cursor.execute(
                        'SELECT records_id FROM records WHERE book_returned="No" AND book_user_id=?',
                        [str(book_id)],
                    )
                    borrowed_books_count = len(cursor.fetchall())

                    if borrowed_books_count < copies:
                        available_book_ids.append(book_id)

                for book_id in available_book_ids:
                    cursor.execute(
                        "SELECT books_name FROM books WHERE book_id=?", [book_id]
                    )
                    book_name = cursor.fetchall()
                    book_names.append(book_name)

                    cursor.execute(
                        "SELECT image, books_name, author FROM books WHERE book_id=?",
                        [book_id],
                    )
                    full_details = cursor.fetchall()
                    book_full_details.append(full_details)

        except Exception as e:
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

            return render_template(
                "display_borrowable_books.html",
                book_names=book_names,
                book_full_details=book_full_details,
            )
