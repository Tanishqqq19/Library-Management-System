from flask import Flask, render_template, request, session
import sqlite3 as sql

def init_app(app):
    @app.route('/search_books_by_author', methods=["GET", "POST"])
    def search_books_by_author():
        # Check if the user is authenticated
        if not session.get('authenticated', False):
            return render_template('login.html', error_message="You haven't logged in")

        if request.method == "POST":
            matching_books = []
            search_query = request.form.get('search')

            try:
                with sql.connect('library.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute('SELECT author, books_name, image FROM books')
                    all_books = cursor.fetchall()

                    for author, book_name, image in all_books:
                        if author.startswith(search_query):
                            matching_books.append((author, book_name, image))
            except Exception as e:
                if connection:
                    connection.rollback()
            finally:
                if connection:
                    connection.close()
                return render_template('display_borrowable_books.html', matching_books=matching_books)

        if request.method == "GET":
            return render_template('display_borrowable_books.html')