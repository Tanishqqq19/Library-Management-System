from flask import Flask, session, render_template
import sqlite3 as sql

def init_app(app):
    @app.route('/admin_records')
    def admin_records():
        # Check if the user is authenticated
        if not session.get('authenticated', False):
            return render_template('login.html', error_message="You haven't logged in")

        records = []
        try:
            # Open a new database connection
            with sql.connect('library.db') as conn:
                cur = conn.cursor()
                cur.execute('SELECT book_user_name, from_date, to_date, borrow_user_name FROM records')
                records = cur.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            # Optionally, you can log the exception here
        finally:
            # The connection is automatically closed after exiting the 'with' block

            return render_template('admin_records.html', records=records)

