# import pymongo
from flask import Flask, request, render_template
from login import login
from admin import admin
from employees import employees
import database_connection

app = Flask(__name__)

###### BluePrint for differernt pages
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(employees, url_prefix="/employees")


@app.route("/<name>")
def home(name):
    return render_template("shared-component/index.html", content = name)

# http://127.0.0.1:5001/
@app.route("/", methods=["GET"])
def hello():
    return render_template("base.html")


# http://127.0.0.1:5001/hello
@app.route("/employees", methods=["GET"])
def greet():
    return "<h1>Hello World</h1>"


# http://127.0.0.1:5001/name
# This should return your name
@app.route("/name", methods=["GET"])
def name():
    print(request)
    return "<h1>Employee Management System</h1>"

if __name__ == '__main__':
    #### Provides all the table names ###############
    get_database_tables = database_connection.overall_connection()

    ############# Calling the employees table an that fetches everything from their respective collections ###############
    database_connection.employee_table(get_database_tables["employee"])
    database_connection.login_table(get_database_tables["login"])
    database_connection.role_table(get_database_tables["role"])

    app.run(port=5001, debug=True)