from flask import Blueprint, render_template, request, session, redirect, url_for, app

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route('shared-component/login.py', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('index', error=error)
    return render_template("index .html")