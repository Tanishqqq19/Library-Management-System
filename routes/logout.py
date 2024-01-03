from flask import session, redirect

def init_app(app):
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')