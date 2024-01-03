from os import error
from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
from flask.templating import _default_template_ctx_processor
from flask_mail import Mail, Message
from datetime import datetime,timedelta,date
from werkzeug.security import generate_password_hash, check_password_hash

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

# C:\Projects\Trial\sqlite-tools-win32-x86-3340100/sqlite3 c:\Users\tanme\Documents\GitHub\Library-Management-System\library.db
"""
The bottom is how the update statement works
update books SET image="https://i.postimg.cc/QMxDrvF8/great-gatsby.jpg" where books_name="Around the World in 80 days";
"""

app= Flask(__name__)
app.config["SECRET_KEY"]="180909090909090909"


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
# The homepage which we see when we open
@app.route('/')
def index():
    return render_template('index.html')
# the admin cans see all the books which were ever borrowed by the user

@app.route('/user_history', methods=["POST","GET"])
def user_history():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    if request.method=="POST":
        user_history=request.form.get('search')
        from_=request.form.get('search1')
        to_=request.form.get('search2')
        # print(from_)
        # print(to_)
        conn=None
        try:
            with sql.connect('library.db') as conn:
                cur=conn.cursor()
                cur.execute('Select books_name, start, end from multiple_book_records where username=?',[user_history])
                records=cur.fetchall()
                print(records)
                if from_!='' and to_!='':
                    mylist=[]
                    for i in records:
                        # print(i[1]>=from_)
                        # print(i[2]>=to_)
                        if i[1]>=from_:
                            if i[2]<=to_:
                                mylist.append([i[0],i[1],i[2]])
                    records=mylist
                

        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
            return render_template('user_history.html',records=records)
    if request.method=="GET":  
        return render_template('user_history.html')




# The page where the admin can see who borrowed which book and when.
@app.route('/admin_records')
def admin_records():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    conn=None
    print(1)
    records=''
    print(2)
    try:
        print(3)
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            print(4)
            cur.execute('Select from_date, to_date, user_id FROM records')
            print(5)
            records=cur.fetchall()
            print(records)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('admin_records.html', records=records)
        

    


if __name__ == '__main__':
    app.run(debug=True)