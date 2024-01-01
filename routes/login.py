from flask import session, render_template, request, redirect
import sqlite3 as sql
from werkzeug.security import check_password_hash
from utils.user_exist import user_exist

def init_app(app):
    @app.route('/login', methods=["POST", "GET"])
    def login():
        if request.method == 'POST':
            print(1)
            email = request.form.get('email')
            password = request.form.get('password')
            print(email, password)
            is_user_existing = user_exist(email)
            print(is_user_existing)
            if is_user_existing:
                try:
                    print(2)
                    with sql.connect('library.db') as connection:
                        cursor = connection.cursor()
                        cursor.execute('SELECT password, user_id, Username FROM register_and_login WHERE email=?', [email])
                        print(4)
                        user_credentials = cursor.fetchone()
                        print(user_credentials)
                        print(5)

                        hashed_password = user_credentials[0]
                        user_id = user_credentials[1]
                        username = user_credentials[2]

                        session["user_id"] = user_id
                        session["Username"] = username

                        is_password_correct = check_password_hash(hashed_password, password)

                        if is_password_correct:
                            try:
                                with sql.connect('library.db') as connection:
                                    cursor = connection.cursor()
                                    cursor.execute('SELECT role FROM register_and_login WHERE user_id=?', [user_id])
                                    user_roles = cursor.fetchall()
                            except Exception as e:
                                connection.rollback()
                            finally:
                                for role_tuple in user_roles:
                                    for role in role_tuple:
                                        session['authenticated'] = True
                                        if role == "admin":
                                            return redirect('/admin_records')
                                        elif role == "user":
                                            return render_template('overview_home.html')
                        else:
                            return render_template('login.html', error_message="Incorrect username or password")
                except Exception as e:
                    if connection:
                        connection.rollback()
                finally:
                    if connection:
                        connection.close()

        return render_template('login.html')
