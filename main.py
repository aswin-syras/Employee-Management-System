# import pymongo
from flask import Flask, request, render_template, url_for
from login import login
from admin import admin
from employees import employees
from flask_pymongo import PyMongo
import database_connection

app = Flask(__name__)

###### BluePrint for differernt pages
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(employees, url_prefix="/employees")

app.config["MONGO_URI"] = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
mongo = PyMongo(app)

fetch_database_connection = database_connection.database_connection()

# connection_string = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
# my_client = pymongo.MongoClient(connection_string)


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


@app.route("/profile")
def profile_pictures():
    return '''
        <form method="POST" action="/create"  enctype="multipart/form-data">
            <input type="text" name="username" />
            <input type="file" name="profile_image" />
            <input type="submit" />
        </form>
    '''

@app.route("/create", methods=['POST'])
def create():
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.users.insert({'username': request.form.get('username'), 'profile_image_name': profile_image.filename})
        return 'DONE!'

@app.route("/file/<filename>")
def file(filename):
    return mongo.send_file(filename)

# @app.route("/profile/<_id>")
# def profile(_id):
#     employees = mongo.db.employees.find_one_or_404({'_id': _id})
#     return f'''
#         <h1>{_id}</h1>
#         <img src="{url_for('file', filename=employees['profile_image_name'])}">
# '''

@app.route("/profiles/<int:id>")
def profile(id):
    # employees = mongo.db.employees.find_one_or_404({'_id': id})
    employees = mongo.db.employees.find_one_or_404({'_id': id})
    print(employees)

    return f'''
        <h1>id</h1>
        <img src="{url_for('file', filename=employees['profile_image_name'])}">
'''

@app.route("/newEmployee")
def createNewEmployeeGET():
    all_roles = database_connection.connect_role_table_name()
    all_managers = database_connection.connect_manager_table_name()
    return render_template("shared-component/new_employee.html", display_all_roles = database_connection.role_table(all_roles), display_all_managers = database_connection.manager_table(all_managers), came_from = "admin.adminHome")


@app.route("/createNewEmployee", methods=['POST'])
def createNewEmployee():
    print(request.form)
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)
        all_employees_table = database_connection.connect_employee_table_name()
        all_emp_record = database_connection.employee_table(all_employees_table)

        mongo.db.employees.insert({'_id': len(all_emp_record) + 1,
                                   'first_name': request.form.get('fName'),
                                   'last_name': request.form.get('lName'),
                                   'phone_number': request.form.get('phoneNumber'),
                                   'email_address': request.form.get('emailAddress'),
                                   'user_role_id': int(request.form.get('role_id')),
                                   'user_manager_id': int(request.form.get('manager_id')),
                                   'profile_image_name': profile_image.filename})
        return 'DONE!'


if __name__ == '__main__':
    #### Provides all the table names ###############
    # get_database_tables = database_connection.overall_connection()

    ############# Calling the employees table an that fetches everything from their respective collections ###############
    # database_connection.employee_table(get_database_tables["employee"])
    # database_connection.login_table(get_database_tables["login"])
    # database_connection.role_table(get_database_tables["role"])

    app.run(port=5001, debug=True)