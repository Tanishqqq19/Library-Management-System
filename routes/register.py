import sqlite3 as sql

from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash

from utils.user_exist import user_exist


def init_app(app):
    @app.route("/register", methods=["POST", "GET"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            is_user_existing = user_exist(email)
            hashed_password = generate_password_hash(password, "sha256")

            if not is_user_existing:
                try:
                    with sql.connect("library.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute(
                            "INSERT INTO register_and_login(Username, password, email, role) VALUES(?,?,?,?)",
                            (username, hashed_password, email, "user"),
                        )
                        connection.commit()
                except Exception as e:
                    if connection:
                        connection.rollback()
                finally:
                    if connection:
                        connection.close()
                    return render_template(
                        "login.html", message="Registration successful, please login"
                    )
            else:
                return render_template(
                    "login.html", error_message="Email already registered. Please login"
                )

        return render_template("register.html")
