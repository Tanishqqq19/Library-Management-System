import sqlite3 as sql
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, session

def borrow_(books):
    if session.get("authenticated", False) == False:
        return render_template("login.html", error_message="You haven't logged in")
    session["books"] = books
    return render_template("booking_page.html", books=books)
