from flask import Flask, render_template
 
from routes.add_book import add_books
from routes.admin_records import admin_records_
from routes.borrow import borrow_
from routes.borrow_duration import borrow_duration_
from routes.display_books import display_books_
from routes.display_borrowable_books import display_borrowable_books_
from routes.faq import faq_
from routes.login import login_user
from routes.logout import logout_
from routes.manage_returns import manage_returns_
from routes.overview_home import overview_home_
from routes.process_return import process_return_
from routes.register import register_user
from routes.search_books_by_author import search_books_by_author_
from routes.search_books_by_title import search_books_by_title_

from routes.display_books_admin import display_books_admin_function

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


# C:\Projects\Trial\sqlite-tools-win32-x86-3340100/sqlite3 c:\Users\tanme\Documents\GitHub\Library-Management-System\library.db


app = Flask(__name__)
# app.config["SECRET_KEY"]="180909090909090909"
app.config["SECRET_KEY"] = (DATABASE_URL)


@app.route("/")
def index(): return render_template("index.html")

@app.route('/display_books')
def display_books(): return display_books_()

@app.route("/search_books_by_title", methods=["POST", "GET"]) # type: ignore
def search_books_by_title(): return search_books_by_title_()

@app.route("/search_books_by_author", methods=["POST", "GET"]) # type: ignore
def search_books_by_author(): return search_books_by_author_()

@app.route("/add_book", methods=["POST", "GET"]) 
def add_book(): return add_books()

@app.route("/register", methods=["POST", "GET"])
def register(): return register_user()

@app.route("/login", methods=["POST", "GET"])
def login(): return login_user()

@app.route("/display_borrowable_books")
def display_borrowable_books(): return display_borrowable_books_()

@app.route("/borrow_duration", methods=['POST'])
def borrow_duration(): return borrow_duration_()

@app.route("/borrow/<books>")
def borrow(books): return borrow_(books)

@app.route("/manage_returns")
def manage_returns(): return manage_returns_()

@app.route("/process_return/<book_id>")
def process_return(book_id): return process_return_(book_id)

@app.route("/logout")
def logout(): return logout_()

@app.route("/faq")
def faq(): return faq_()

@app.route("/overview_home")
def overview_home(): return overview_home_()

@app.route("/admin_records")
def admin_records(): return admin_records_()

@app.route("/display_books_admin")
def display_books_admin_(): return display_books_admin_function()

if __name__ == "__main__":
    app.run(debug=True)
