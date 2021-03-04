from flask import Blueprint, render_template

employees = Blueprint("employees", __name__, static_folder="static", template_folder="templates")

@employees.route("/")
def home():
    return render_template("employees/employee.html")

def latestfn():
    print("cd")