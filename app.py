from os import error
from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
from flask.templating import _default_template_ctx_processor
from flask_mail import Mail, Message
from datetime import datetime,timedelta,date
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from routes.register import init_app as register_init_app
from routes.display_books import init_app as display_books_init_app
from routes.login import init_app as login_init_app
from routes.display_borrowable_books import init_app as display_borrowable_books_init_app

# C:\Projects\Trial\sqlite-tools-win32-x86-3340100/sqlite3 c:\Users\tanme\Documents\GitHub\Library-Management-System\library.db
"""
The bottom is how the update statement works
update books SET image="https://i.postimg.cc/QMxDrvF8/great-gatsby.jpg" where books_name="Around the World in 80 days";
"""

app= Flask(__name__)
app.config["SECRET_KEY"]="180909090909090909"

# A button which will help you log out from your account
@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')


# The q and a of the things in the system
@app.route('/qanda')
def qanda():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    else:
        return render_template('qanda.html')

# searching all the books available


# These are all the books the admin can see.
display_books_init_app(app)

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





# The first page the user sees after he logs in
@app.route('/overview_home')
def overview_home():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    return render_template('overview_home.html')

#registration 
register_init_app(app)

# login
login_init_app(app)

# This is the page where the user can borrow books. The opening one.
display_borrowable_books_init_app(app)

# The page where the admin can see who borrowed which book and when.
@app.route('/admin_records')
def admin_records():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    conn=None
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select books_name, start, end, username from multiple_book_records')
            records=cur.fetchall()
            # mylist=[]
            for i in records:
                print(i)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('admin_records.html')
# This is the page of all the books the user can see

# This is the page where the person can return the books
@app.route('/return_book')
def return_book(): 
    conn=None
    user_id=session['user_id']
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            user_id=session['user_id']
            # cur.execute()
            cur.execute('Select book_user_id from records where book_returned="No" and borrow_user_id=?',[user_id])
            rec=cur.fetchall()
            print(rec)
            print('-----------')
            mylist=[]
            for i in rec:
                for j in i:
                    cur.execute('Select image,book_id, author from books where book_id=?',[j])
                    my=cur.fetchall()
                    for i in my:
                        mylist.append(i)
            print(mylist)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('return.html',mylist=mylist)

@app.route('/booking/<books>')
def booking(books):
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    session['books']=books   
    all_the_dates=[]
    for i in range(1,6):
        dt=datetime.datetime.today() + datetime.timedelta(days=i)
        g=dt.date()
        all_the_dates.append(g)
    return render_template('booking_page.html',books=books,all_the_dates=all_the_dates)

# The returning book page 
@app.route('/returning/<book>')
def returning(book):
    conn=None
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    session['book_id']=book
    user_id=session['user_id']
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            print(book)
            # update books SET image="https://i.postimg.cc/QMxDrvF8/great-gatsby.jpg" where books_name="Around the World in 80 days";
            today=date.today()
            yesterday=today + datetime.timedelta(days=-10)
            # cur.execute('INSERT INTO records(book_user_id, borrow_user_id, from_date,to_date,book_returned) Values(?,?,?,?,?)',(book,user_id, yesterday,today,"No"))
            # records=cur.fetchall()
            print("PASSED #1")
            jem="Select records_id from records where book_user_id= "+book+" and book_returned='No' and borrow_user_id="+str(user_id)+";"
            print(jem)
            cur.execute(jem)
            records=cur.fetchall()
            print(records)
            print("PASSED #2")
            # jem1='update records SET to_date='+today+' and book_returned="Yes" where borrow_user_id= '+user_id+' and book_returned="No";'
            # print(jem1)
            for i in records:
                for j in i:
                    print(yesterday)
                    jem1='update records SET from_date="'+str(yesterday)+'" where borrow_user_id='+str(user_id)+' and book_returned="No" and records_id='+str(j)+';'
                    print(jem1)
                    cur.execute(jem1)
                    jem2='update records SET to_date="'+str(yesterday)+'" where borrow_user_id='+str(user_id)+' and book_returned="No" and records_id='+str(j)+';'
                    print(jem2)
                    cur.execute(jem2)
                    jem1='update records SET book_returned="Yes" where borrow_user_id='+str(user_id)+' and book_returned="No" and records_id='+str(j)+';'
                    print(jem1)
                    cur.execute(jem1)
                    break
                break
            print("PASSED #3")
            ask1="Select from_date, to_date from records where book_user_id="+book+" and borrow_user_id="+str(user_id)+" and book_returned='No';"
            print(ask1)
            cur.execute(ask1)
            extra_one=cur.fetchall()
            print(extra_one)
            cur.execute('Select books_name, author,image from books where book_id=?',[book])
            extra_two=cur.fetchall()
            print(extra_one)
            print(extra_two)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('returning_page.html',ret="return was successful",extra_one=extra_one,extra_two=extra_two)
# This page is shown if the return was successful
@app.route('/return_successful',methods=["POST","GET"])
def return_successful():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    if request.method=="GET":
        return render_template('overview_home.html')
    if request.method=="POST":
        conn=None
        answer=request.form.get('answer')
        if answer=="NO":
            return render_template('overview_home.html')
        if answer=="YES":
            today=date.today()
            print(today)
            f=str(today)
            print(f)
            print(type(f))
            book=session['book_id']
            print('-------------')
            print(book)
            print('----------------')
            # update books SET image="https://i.postimg.cc/QMxDrvF8/great-gatsby.jpg" where books_name="Around the World in 80 days";
            try:
                with sql.connect('library.db') as conn:
                    cur=conn.cursor()
                    print('update multiple_book_records SET end="'+f+' "where user_id='+book+';')
                    cur.execute('update multiple_book_records SET start="24-7-21" where user_id='+book+';')
                    cur.execute('update multiple_book_records SET end="25-7-21" where user_id='+book+';')
                    cur.execute('update multiple_book_records SET username="Jane" where user_id='+book+';')
                    cur.execute('update multiple_book_records SET first_name=0 where user_id='+book+';')
                    cur.execute('Select books_name from multiple_book_records where user_id=?',[book])
                    records=cur.fetchall()
                    print(records)
            except Exception as e:
                conn.rollback()
            finally:
                conn.close()
            return render_template('overview_home.html')
# This code will help in telling if you can borrow the book for onw week.
@app.route('/duration/<time_period>')
def one_week():
    books=session['books']
    print(books)
    user_id=session['user_id']
    conn=None
    try:
        with sql.connect('library.db') as conn:

            cur=conn.cursor()
            cur.execute("Select copies, book_id from books where books_name=?",[books])
            rec=cur.fetchall()
            for i in rec:
                copies=i[0]
                book_id=i[1]


            from datetime import date
            today = date.today()
            week=today + datetime.timedelta(days=7)
            num=0
            cur.execute('Select from_date, to_date from records where book_returned="No" and book_user_id=?',[book_id])
            dates=cur.fetchall()
            print(len(dates))
            for i in dates:
                if (len(dates)-1)>=copies:
                    return render_template('one_week.html',ref="Sorry you cannot borrow")
                if str(today)>i[0]:
                    cur.execute('INSERT INTO records(book_user_id, borrow_user_id, from_date,to_date,book_returned) Values(?,?,?,?,?)',(book_id,user_id, today,week,"No"))
                    return render_template('one_week.html',ref="borrowed")
            

    except Exception as e:
        conn.rollback()
    finally:     
        conn.close()
        # return render_template('one_week.html',ref="doesn't work")


# The place where the admin can add more books
@app.route('/add_book', methods=["POST","GET"])
def add_book():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    conn=None
    user_id=session['user_id']
    username=session['Username']
    if request.method=="GET":
        return render_template('add_book.html')
    if request.method=="POST":
        book=request.form.get('book')
        image=request.form.get("image")
        quantity=request.form.get('quantity')
        author=request.form.get('author')
        try:
            with sql.connect('library.db') as conn:
                cur=conn.cursor()
                """
                INSERT INTO books(books_name, start, end, user_id, image) Values(?,?,?,?,?),('Audacity of Hope','24-7-21','25-7-21','Tanishq Security Key','https://i.postimg.cc/Qxg6JrjD/audacity.jpg')
                """
                print(12)
                import datetime
                from datetime import date
                today = date.today()
                print(today)
                yesterday=today + datetime.timedelta(days=-1)
                print(yesterday)
                two_days=today+datetime.timedelta(days=-2)
                print(two_days)
                # Inserting the book into the database
                cur.execute('INSERT INTO books(books_name,author, copies, image) Values(?,?,?,?)',(str(book),author,quantity,str(image)))
                print(22)
                # To get the user_id from the books. So, that I can 
                cur.execute("Select book_id from books where books_name=?",[book])
                records=cur.fetchall()
                print(records)
                for i in records:
                    for j in i:
                        print(j)
                print("PASS1")
                cur.execute('INSERT INTO records(book_user_id,borrow_user_id, from_date, to_date,book_returned) Values(?,?,?,?,?)',(j,user_id,two_days,yesterday,"No"))
                print("PASS")
                print(32)
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
            return render_template('add_book.html')


if __name__ == '__main__':
    app.run(debug=True)