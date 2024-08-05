from flask import Flask, render_template, request, session
import sqlite3 as sql


def display_books_():
    if not session.get('authenticated', False):
        return render_template('login.html', error_message="You haven't logged in")
    unique_book_images=[]
    titles=[]
    try:
        with sql.connect('library.db') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT image, author, books_name from books')
            book_images = cursor.fetchall()   
            for image,author,title in book_images:
                if title not in titles:
                    titles.append(title)
                    unique_book_images.append([image,author,title])

    except Exception as e:
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()

        return render_template('display_books.html', book_images=unique_book_images)

