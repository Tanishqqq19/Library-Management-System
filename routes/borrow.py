from flask import Flask, render_template, request, session
import sqlite3 as sql
from datetime import datetime,timedelta,date

def init_app(app):
    @app.route('/borrow/<books>')
    def borrow(books):
        if session.get('authenticated',False)==False:
            return render_template('login.html',error_message="You haven't logged in")
        session['books']=books
        print(books)   

        return render_template('booking_page.html',books=books)