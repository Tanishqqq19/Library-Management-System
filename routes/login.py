import sqlite3 as sql

from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash

from utils.user_exist import user_exist



def login_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email,password)

        if password==None:
            return render_template(
                            "login.html",
                            error_message="Password returns None",
                        )
        print(1)
        is_user_existing = user_exist(email)
        print(2)
        if is_user_existing:
            try:
                with sql.connect("library.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "SELECT password, user_id, Username FROM register_and_login WHERE email=?",
                        [email],
                    )
                    print(3)
                    user_credentials = cursor.fetchone()
                    hashed_password = user_credentials[0]
                    user_id = user_credentials[1]
                    username = user_credentials[2]
                    print(4)
                    print(user_credentials)

                    session["user_id"] = user_id
                    session["Username"] = username
                    print(5)
                    print(hashed_password, password)
                    is_password_correct = check_password_hash(hashed_password, password)
                    print(is_password_correct)
                    if is_password_correct:
                        try:
                            with sql.connect("library.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute(
                                    "SELECT role FROM register_and_login WHERE user_id=?",
                                    [user_id],
                                )
                                user_roles = cursor.fetchall()
                        except Exception as e:
                            connection.rollback()
                        finally:
                            for role_tuple in user_roles:
                                for role in role_tuple:
                                    session["authenticated"] = True
                                    if role == "admin":
                                        print(1)
                                        return redirect("/admin_records")
                                    elif role == "user":
                                        return render_template("overview_home.html")
                    else:
                        return render_template(
                            "login.html",
                            error_message="Incorrect username or password",
                        )
            except Exception as e:
                if connection:
                    connection.rollback()
            finally:
                if connection:
                    connection.close()

    return render_template("login.html")
