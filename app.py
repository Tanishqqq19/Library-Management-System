from os import error
from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
from flask.templating import _default_template_ctx_processor
from flask_mail import Mail, Message
from datetime import datetime,timedelta,date
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
# C:\Projects\Trial\sqlite-tools-win32-x86-3340100/sqlite3 c:\Users\tanme\Desktop\Lib_pro\library.db
"""
The bottom is how the update statement works
update books SET image="https://i.postimg.cc/QMxDrvF8/great-gatsby.jpg" where books_name="Around the World in 80 days";
"""
import random
import os
import smtplib
import imghdr
from email.message import EmailMessage

def email():
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    contacts = ['YourAddress@gmail.com', 'test@example.com']

    msg = EmailMessage()
    msg['Subject'] = 'Forgot password'
    msg['From'] = 'tanmeup195@gmail.com'
    msg['To'] = 'eciatma@gmail.com'
    l=random.randint(10000,100000)
    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
            <h4>Password:</h4>"""""+str(l)+"""
            <h4>for further continuance go here</h4>
        <a href="/http://127.0.0.1:5000/forgot_password">
        </a>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("tanmeup195@gmail.com", "Networking1$")
        smtp.send_message(msg)

app= Flask(__name__)
app.config["SECRET_KEY"]="180909090909090909"

# A function check which will check if the same user isn't logging in again 
def user_exist(email):
    conn=None
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select email from register_and_login where email=?',[email])
            records=cur.fetchall()
            if len(records)>0:
                return True
            else:
                return False
    except Exception as e:
        conn.rollback()
        n='operation unsuccessful'
    finally:
        conn.close()
# To check if a person is a user or a admin
def check_role():
        conn=None
        try:
            user_id=session['user_id']
            with sql.connect('library.db') as conn:
                cur=conn.cursor()
                for i in books:
                    cur.execute('Select role from register_and_login where user_id=?'+user_id)
                    records=cur.fetchall()
                    return records
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
# A button which will help you log out from your account
@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

# Getting the email for the password
@app.route('/get_email',methods=["POST","GET"])
def get_email():
    if request.method=="POST":
        email=request.form.get("email")
        print(email)
        return render_template('forgotpassword.html')
    if request.method=="GET":
        email=request.form.get("email")
        print(email)
        return render_template('get_email.html')


# Forgot password
@app.route('/forgot_password',methods=["POST","GET"])
def forgot_password():
    if request.method=="POST":
        email=request.form.get("email")
        print(email)
        session['email_save']=email
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

        contacts = ['YourAddress@gmail.com', 'test@example.com']

        msg = EmailMessage()
        msg['Subject'] = 'Forgot password'
        msg['From'] = 'tanmeup195@gmail.com'
        msg['To'] = email
        l=random.randint(10000,100000)
        session['l']=l
        msg.set_content('This is a plain text email')

        msg.add_alternative("""\
                <h4>Password:</h4>"""""+str(l)+"""
                <h4>for further continuance go here</h4>
            <a href="http://127.0.0.1:5000/forgot_password">
            </a>
        """, subtype='html')


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("tanmeup195@gmail.com", "Networking1$")
            smtp.send_message(msg)
        return render_template('forgotpassword1.html')
    if request.method=="GET":
        # email=request.form.get('email')
        # print(email)
        return render_template('forgotpassword.html') 

@app.route('/forgot_password1', methods=["POST","GET"])
def forgot_password1():
    if request.method=="POST":
        password=request.form.get('password')
        j=int(password)
        print(j)
        print(type(j))
        f=session['l']
        print(f)
        print(type(f))
        if j==f:
            return render_template('change_password.html')
        else:
            return render_template('forgotpassword1.html',error="wrong_password")
    if request.method=="GET":
        return render_template('forgotpassword1.html')
@app.route('/change_password', methods=["POST","GET"])
def change_password():
    if request.method=="POST":
        update=request.form.get("password")
        print(update)
        email=session['email_save']
        print(email)
        return render_template('change_password.html')
    if request.method=="GET":
        return render_template('change_password.html')

# An about page of me
@app.route('/about')
def about():
    return render_template('about.html')
# The q and a of the things in the system
@app.route('/qanda')
def qanda():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    else:
        return render_template('qanda.html')

# searching all the books available
@app.route('/book_search',methods=["POST","GET"])
def book_search():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    if request.method=="POST":
        conn=None
        mylist=[]
        try:
            with sql.connect('library.db') as conn:
                cur=conn.cursor()
                search=request.form.get('search')
                print(search)
                cur.execute('Select books_name,image from books')
                s=cur.fetchall()
                g=len(search)
                for i in s:
                    j=i[0]
                    if j[:g]==search:
                        mylist.append(i)
                print(mylist)
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
            return render_template('books.html',mylist=mylist)
    if request.method=="GET":
        conn=None
        return render_template('books.html')


@app.route('/book_search_author',methods=["GET","POST"])
def book_search_author():
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    if request.method=="POST":
        conn=None
        mylist=[]
        try:
            with sql.connect('library.db') as conn:
                cur=conn.cursor()
                search=request.form.get('search')
                print(search)
                cur.execute('Select author,books_name,image from books')
                s=cur.fetchall()
                g=len(search)
                for i in s:
                    j=i[0]
                    if j[:g]==search:
                        mylist.append(i)
                print(mylist)
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()
            return render_template('books.html',records3=mylist)
    if request.method=="GET":
        conn=None
        return render_template('books.html')

# These are all the books the admin can see.
@app.route('/all_the_books2')
def all_the_books2():
    conn=None
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select image from books')
            records2=cur.fetchall()
            records2=set(records2)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('all_the_books2.html',records2=records2)

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
@app.route('/register', methods=["POST","GET"])
def registration():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')        
        conn=None
        return_value=user_exist(email)
        secret_password=generate_password_hash(password, "sha256")
        if return_value==False:
            try:
                with sql.connect('library.db') as conn:
                        cur=conn.cursor()
                        # in role if 1 ur admin and if 2 ur user
                        cur.execute('INSERT INTO register_and_login(Username, password, email, role) Values(?,?,?,?)',(username, secret_password, email, "user"))
                        conn.commit()
            except Exception as e:
                    conn.rollback()
            finally:
                conn.close()
                return render_template('login.html')
        else:
            return render_template('login.html', error_message="You have already signed in once please login")
    if request.method=="GET":
        return render_template('register.html')


# login
@app.route('/login', methods=["POST","GET"])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    conn=None
    m=user_exist(email)
    if m==True:
        if request.method=='POST':
            try:
                with sql.connect('library.db') as conn:
                    cur=conn.cursor()
                    cur.execute('Select password,user_id,Username from register_and_login where email=?',[email])
                    records=cur.fetchone()
                    print(records)
                    conn.commit()
                    correct_password=records[0]
                    user_id=records[1]
                    user_name=records[2]
                    session["user_id"]=user_id
                    session["Username"]=user_name
                    uncover_password=check_password_hash(correct_password, password)
                    if uncover_password==True:
                        try:
                            user_id=session['user_id']
                            with sql.connect('library.db') as conn:
                                cur=conn.cursor()
                                cur.execute('Select role from register_and_login where user_id=?',[user_id])
                                records2=cur.fetchall()
                        except Exception as e:
                            conn.rollback()
                        finally:
                            for i in records2:
                                for j in i:
                                    session['authenticated']=True
                                    if j=="admin":
                                        conn.close()
                                        return redirect('/admin_records')
                                    if j=="user":
                                        conn.close()
                                        return render_template('overview_home.html')
                    else:
                        return render_template ('login.html',error_message="The Username or the Password is wrong")
            except Exception as e:
                    conn.rollback()
            finally:
                conn.close()
        if request.method=="GET":
            return render_template('login.html')
    else:
        return render_template('login.html')


# This is the page where the user can borrow books. The opening one.
@app.route('/books')
def books():   
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    conn=None
    records1=""
    records2=""
    jem=""
    print('This works')
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select book_id, copies from books')
            jem=cur.fetchall()
            mylist=[]
            mylist1=[]
            mylist2=[]
            for i in jem:
                cur.execute('select records_id from records where book_returned="No" and book_user_id=?',[str(i[0])])
                re=cur.fetchall()

                if (len(re)-1)<i[1]:
                    # print(len(re),i[0])
                    mylist.append(i[0])
            print(mylist)
            for i in mylist:
                # print('Select books_name from books where book_id=?',[i])
                cur.execute('Select books_name from books where book_id=?',[i])
                records1=cur.fetchall()
                mylist1.append(records1)
            # print('-------')
            # print(mylist1)
            # print('-------')
            for i in mylist:
                # print('Passed 1')
                cur.execute('Select image,books_name,author from books where book_id=?',[i])
                # print('Passed 2')
                records2=cur.fetchall()
                # print(records2)
                mylist2.append(records2)
            # print(mylist2)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('books.html',records1=mylist1,records2=mylist2)

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
@app.route('/all_the_books')
def all_the_books():
    conn=None
    if session.get('authenticated',False)==False:
        return render_template('login.html',error_message="You haven't logged in")
    try:
        with sql.connect('library.db') as conn:
            cur=conn.cursor()
            cur.execute('Select image from books')
            records2=cur.fetchall()
            records2=set(records2)
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
        return render_template('all_the_books.html',records2=records2)


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
@app.route('/one_week')
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

@app.route('/two_week')
def two_week():
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
            two_week=today + datetime.timedelta(days=14)
            num=0
            cur.execute('Select from_date, to_date from records where book_returned="No" and book_user_id=?',[book_id])
            dates=cur.fetchall()
            print(len(dates))
            for i in dates:
                if (len(dates)-1)>=copies:
                    return render_template('one_week.html',ref="Sorry you cannot borrow")
                if str(today)>i[0]:
                    cur.execute('INSERT INTO records(book_user_id, borrow_user_id, from_date,to_date,book_returned) Values(?,?,?,?,?)',(book_id,user_id, today,two_week,"No"))
                    return render_template('one_week.html',ref="borrowed")
            

    except Exception as e:
        conn.rollback()
    finally:     
        conn.close()
        # return render_template('one_week.html',ref="doesn't work")

@app.route('/one_month')
# def borrow_for_time(num_days):         
def one_month():
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
            # Change the 30 to num_days
            one_month=today + datetime.timedelta(days=30)
            num=0
            cur.execute('Select from_date, to_date from records where book_returned="No" and book_user_id=?',[book_id])
            dates=cur.fetchall()
            print(len(dates))
            for i in dates:
                if (len(dates)-1)>=copies:
                    return render_template('one_week.html',ref="Sorry you cannot borrow")
                if str(today)>i[0]:
                    cur.execute('INSERT INTO records(book_user_id, borrow_user_id, from_date,to_date,book_returned) Values(?,?,?,?,?)',(book_id,user_id, today,one_month,"No"))
                    return render_template('one_week.html',ref="borrowed")
            

    except Exception as e:
        conn.rollback()
    finally:     
        conn.close()
# @app.route('/book_search_author',methods=["POST","GET"])
# def book_search_author():

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