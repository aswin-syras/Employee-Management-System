from flask import Blueprint, render_template, request, session, redirect, url_for, app

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route('/login', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return 'You are logged in as' + session['username']
    return render_template('shared-component/login.html')
