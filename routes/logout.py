from flask import redirect, session


def init_app(app):
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
