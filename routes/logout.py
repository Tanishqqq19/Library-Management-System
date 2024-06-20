from flask import redirect, session


def logout_():
    session.clear()
    return redirect("/")
