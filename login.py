from flask import Blueprint, render_template

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route("/")
def home():
    return render_template("login.html")



#ssssssssssssss