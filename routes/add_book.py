from flask import Flask, render_template, request, session
import sqlite3 as sql
from datetime import date, timedelta

app = Flask(__name__)
def init_app(app):
    @app.route('/add_book', methods=["POST", "GET"])
    def add_book():
        # Check if the user is authenticated
        if not session.get('authenticated', False):
            return render_template('login.html', error_message="You haven't logged in")

        # Database connection setup
        connection = None
        user_id = session['user_id']
        username = session['Username']  # It seems 'username' is not used in this function


        if request.method == "GET":
            return render_template('add_book.html')

        if request.method == "POST":
            book_name = request.form.get('book')
            book_image = request.form.get("image")
            book_quantity = request.form.get('quantity')
            book_author = request.form.get('author')
            try:
                with sql.connect('library.db') as connection:
                    cursor = connection.cursor()

                    # Current and previous dates
                    today = date.today()
                    yesterday = today - timedelta(days=1)
                    two_days_ago = today - timedelta(days=2)

                    # Inserting the book into the database
                    cursor.execute('INSERT INTO books(books_name, author, copies, image) VALUES (?, ?, ?, ?)',(book_name, book_author, book_quantity, book_image))

                    # Retrieve the recently added book's ID
                    cursor.execute("SELECT book_id FROM books WHERE books_name = ?", [book_name])
                    book_id_records = cursor.fetchall()
                    # Assuming only one record is fetched since book names are unique
                    book_id = book_id_records[0][0] if book_id_records else None


                    # Insert record into records table
                    cursor.execute('INSERT INTO records(book_user_id, book_user_name, borrow_user_id, borrow_user_name,from_date, to_date, book_returned) VALUES (?, ?, ?, ?, ?, ?, ?)',(book_id, book_name, user_id, username,two_days_ago, yesterday, "No"))

            except Exception as e:
                if connection:
                    connection.rollback()
                # Consider logging the exception here
            finally:
                if connection:
                    connection.close()
                return render_template('add_book.html')
