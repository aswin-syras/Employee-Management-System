from flask import Blueprint, render_template, request, session, redirect, url_for, app

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
users = []
users.append((User(username="aswin" , password="password")))

@login.route("/login.py", methods=['GET',"POST"])
def home():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        if username == "aswin":
            return redirect(url_for('login'))


    return render_template("login .html")