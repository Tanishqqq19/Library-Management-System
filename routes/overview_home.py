import sqlite3 as sql

from flask import Flask, render_template, request, session

def overview_home_():
    if session.get("authenticated", False) == False:
        return render_template("login.html", error_message="You haven't logged in")
    return render_template("overview_home.html")
