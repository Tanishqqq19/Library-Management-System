from flask import Flask, render_template, request, session
import sqlite3 as sql


def display_books_():
    try:
        with sql.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT image from books')
            book_images = cursor.fetchall()
            unique_book_images = set(book_images)
    except Exception as e:
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()

        return render_template('display_books.html', book_images=unique_book_images)

