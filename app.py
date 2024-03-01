from flask import Flask, render_template
from routes.register import init_app as register_init_app
from routes.display_books import init_app as display_books_init_app
from routes.login import init_app as login_init_app
from routes.display_borrowable_books import init_app as display_borrowable_books_init_app
from routes.search_books_by_title import init_app as search_books_by_title_init_app
from routes.search_books_by_author import init_app as search_books_by_author_init_app
from routes.add_book import init_app as add_book_init_app
from routes.borrow_duration import init_app as borrow_duration_init_app
from routes.borrow import init_app as borrow_init_app
from routes.manage_returns import init_app as manage_returns_init_app
from routes.process_return import init_app as process_return_init_app
from routes.logout import init_app as logout_init_app
from routes.faq import init_app as faq_init_app
from routes.overview_home import init_app as overview_home_init_app
from routes.admin_records import init_app as admin_records_init_app

# C:\Projects\Trial\sqlite-tools-win32-x86-3340100/sqlite3 c:\Users\tanme\Documents\GitHub\Library-Management-System\library.db


app= Flask(__name__)
app.config["SECRET_KEY"]="180909090909090909"

@app.route('/')
def index():
    return render_template('index.html')

display_books_init_app(app)
search_books_by_title_init_app(app)
search_books_by_author_init_app(app)
add_book_init_app(app)
register_init_app(app)
login_init_app(app)
display_borrowable_books_init_app(app)
borrow_duration_init_app(app)
borrow_init_app(app)
manage_returns_init_app(app)
process_return_init_app(app)
logout_init_app(app)
faq_init_app(app)
overview_home_init_app(app)
admin_records_init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)