from flask import Flask, render_template, request, session
import sqlite3 as sql
def init_app(app):
    @app.route('/search_books_by_title', methods=["POST", "GET"])
    def search_books_by_title():
        # Check if the user is authenticated
        if not session.get('authenticated', False):
            return render_template('login.html', error_message="You haven't logged in")

        if request.method == "POST":
            search_query = request.form.get('search').strip()
            books_matching_title = []

            try:
                with sql.connect('library.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute('SELECT books_name, image FROM books')
                    all_books = cursor.fetchall()

                    for book_name, image in all_books:
                        if book_name.startswith(search_query):
                            books_matching_title.append((book_name, image))
                    print(books_matching_title)

            except Exception as e:
                if connection:
                    connection.rollback()
            finally:
                if connection:
                    connection.close()
                return render_template('display_books.html', books_matching_title=books_matching_title)

        if request.method == "GET":
            return render_template('display_books.html')

#this is mylist