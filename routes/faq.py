from flask import render_template, session
def init_app(app):
    @app.route('/faq')
    def faq():
        if session.get('authenticated',False)==False:
            return render_template('login.html',error_message="You haven't logged in")
        else:
            return render_template('faq.html')