import pymongo
from flask import Flask, request, render_template
from login import login
from admin import admin
from employees import employees

app = Flask(__name__)

###### BluePrint for differernt pages
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(employees, url_prefix="/employees")

def connection_db():
    connection_string = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    database_name = my_client["EmployeeManagementSystem"]
    login_table_name = database_name["login"]
    fetch_values = login_table_name.find()
    login_user = [record for record in fetch_values]
    print(login_user)


@app.route("/<name>")
def home(name):
    return render_template("shared-component/index.html", content = name)

# http://127.0.0.1:5001/
@app.route("/", methods=["GET"])
def hello():
    return render_template("base.html")


# http://127.0.0.1:5001/hello
@app.route("/hello", methods=["GET"])
def greet():
    return "<h1>Hello World</h1>"


# http://127.0.0.1:5001/name
# This should return your name
@app.route("/name", methods=["GET"])
def name():
    print(request)
    return "<h1>Employee Management System</h1>"

if __name__ == '__main__':
    connection_db()
    app.run(port=5001, debug=True)