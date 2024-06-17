import sqlite3 as sql

from flask import Flask, render_template, request, session


def init_app(app):
    @app.route("/overview_home")
    def overview_home():
        if session.get("authenticated", False) == False:
            return render_template("login.html", error_message="You haven't logged in")
        return render_template("overview_home.html")
