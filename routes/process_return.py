import sqlite3 as sql
from datetime import date, datetime, timedelta

from flask import Flask, render_template, request, session


def init_app(app):
    @app.route("/process_return/<book_id>")
    def process_return(book_id):
        if not session.get("authenticated", False):
            return render_template("login.html", error_message="You haven't logged in")

        session["book_id"] = book_id
        user_id = session["user_id"]
        try:
            with sql.connect("library.db") as conn:
                cur = conn.cursor()
                today = date.today()
                hundred_days_ago = today - timedelta(days=100)
                records_query = (
                    "SELECT records_id FROM records "
                    "WHERE book_user_id = ? AND book_returned = 'No' "
                    "AND borrow_user_id = ?;"
                )
                cur.execute(records_query, (book_id, user_id))
                records = cur.fetchall()

                for (record_id,) in records:
                    update_query = (
                        "UPDATE records SET from_date = ?, to_date = ?, "
                        "book_returned = 'Yes' "
                        "WHERE borrow_user_id = ? AND book_returned = 'No' "
                        "AND records_id = ?;"
                    )
                    cur.execute(
                        update_query,
                        (hundred_days_ago, hundred_days_ago, user_id, record_id),
                    )
                    break

                book_details_query = (
                    "SELECT books_name, author, image FROM books " "WHERE book_id = ?;"
                )
                cur.execute(book_details_query, (book_id,))
                book_details = cur.fetchall()

        except Exception as e:
            conn.rollback()
            book_details = []
        finally:
            conn.close()

        return render_template(
            "returning_page.html",
            ret="Return was successful",
            book_details=book_details,
        )
