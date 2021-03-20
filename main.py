# import pymongo
from flask import Flask, request, render_template, url_for,session,redirect
from login import login
from admin import admin
from employees import employees
from flask_pymongo import PyMongo
import database_connection
import json
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = "$%^&U$%^TYURTFY&*GU"

###### BluePrint for differernt pages
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(employees, url_prefix="/employees")

app.config["MONGO_URI"] = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
mongo = PyMongo(app)

fetch_database_connection = database_connection.database_connection()

#### Fetch only certain table
all_roles = database_connection.connect_role_table_name()
all_managers = database_connection.connect_manager_table_name()

gender_array = [ 'Not Ready to Declare', 'Male', 'Female']

class InformForm(FlaskForm):
    startdate = DateField('Start Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')


@app.route("/<name>")
def home(name):
    return render_template("shared-component/index.html", content = name)

# http://127.0.0.1:5001/
@app.route("/", methods=["GET"])
def hello():
    return render_template("base.html")

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("shared-component/login.html")


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
    # all_roles = database_connection.connect_role_table_name()
    # all_managers = database_connection.connect_manager_table_name()
    return render_template("shared-component/new_employee.html",
                           display_all_roles = database_connection.role_table(all_roles),
                           display_all_managers = database_connection.manager_table(all_managers),
                           came_from = "admin.adminHome",
                           gender_array = gender_array)

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
                                   'gender': request.form.get('gender'),
                                   'profile_image_name': profile_image.filename})
        return 'DONE!'

@app.route("/editEmployee/<int:id>")
def editEmployee(id):
    #Fetch only the particular employee whose Id matches in the database
    find_one = database_connection.fetch_only_one_employee(id)

    return render_template("shared-component/edit_employee.html",
                            one_employee = find_one,
                           display_all_roles = database_connection.role_table(all_roles),
                           display_all_managers = database_connection.manager_table(all_managers),
                           came_from = "admin.adminHome",
                           gender_array = gender_array)

@app.route("/editAnEmployee/<int:id>", methods=['POST'])
def editAnEmployee(id):
    # print()
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)

        found_one_from_db_before_json = mongo.db.employees.find_one({"_id": id})

        converted_json = json.dumps(found_one_from_db_before_json, sort_keys=True)
        fetched_value_before_json = {
            '_id': id,
            'first_name': request.form.get('fName'),
            'last_name': request.form.get('lName'),
            'phone_number': request.form.get('phoneNumber'),
            'email_address': request.form.get('emailAddress'),
            'user_role_id': int(request.form.get('role_id')),
            'user_manager_id': int(request.form.get('manager_id')) if found_one_from_db_before_json["user_manager_id"] else found_one_from_db_before_json["user_manager_id"],
            'gender': request.form.get('gender'),
            'profile_image_name': profile_image.filename if profile_image.filename else found_one_from_db_before_json["profile_image_name"]
        }

        fetched_val_json = json.dumps(fetched_value_before_json, sort_keys=True)

        collect_data_to_append = {}
        if converted_json == fetched_val_json :
            print("They are Exactly the same, so don't update the db")
        else:
            if ( fetched_value_before_json["first_name"] != found_one_from_db_before_json["first_name"] ):
                collect_data_to_append["first_name"] = fetched_value_before_json["first_name"]
            if (fetched_value_before_json["last_name"] != found_one_from_db_before_json["last_name"]):
                collect_data_to_append["last_name"] = fetched_value_before_json["last_name"]
            if (fetched_value_before_json["phone_number"] != found_one_from_db_before_json["phone_number"]):
                collect_data_to_append["phone_number"] = fetched_value_before_json["phone_number"]
            if (fetched_value_before_json["email_address"] != found_one_from_db_before_json["email_address"]):
                collect_data_to_append["email_address"] = fetched_value_before_json["email_address"]
            if (fetched_value_before_json["user_role_id"] != found_one_from_db_before_json["user_role_id"]):
                collect_data_to_append["user_role_id"] = fetched_value_before_json["user_role_id"]
            if (fetched_value_before_json["user_manager_id"] != found_one_from_db_before_json["user_manager_id"]):
                collect_data_to_append["user_manager_id"] = fetched_value_before_json["user_manager_id"]
            if (fetched_value_before_json["gender"] != found_one_from_db_before_json["gender"]):
                collect_data_to_append["gender"] = fetched_value_before_json["gender"]
            if (fetched_value_before_json["profile_image_name"] != found_one_from_db_before_json["profile_image_name"]):
                collect_data_to_append["profile_image_name"] = fetched_value_before_json["profile_image_name"]

            mongo.db.employees.update_one(
                        { '_id': id },
                        { '$set': collect_data_to_append }
                    )

        #TODO: Need to redirect it to the desired location
        return render_template("shared-component/index.html")

@admin.route("/createnewEvent", methods=['GET', 'POST'])
def return_data():
    return ()

@app.route("/createNewEventPost", methods=['GET', 'POST'])
def createNewEventPost():
    form = InformForm()
    if (form.validate_on_submit()):
        print("CLISEKED SUBMIT")
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        return redirect(url_for("date"))
    return render_template('admin/new_event_creation.html', form=form)

@app.route("/date", methods=['POST'])
def date():
    form = InformForm()
    session['startdate'] = form.startdate.data
    session['enddate'] = form.enddate.data
    startdate = session["startdate"]
    enddate = session["enddate"]

    return render_template('admin/date.html')

if __name__ == '__main__':
    #### Provides all the table names ###############
    # get_database_tables = database_connection.overall_connection()

    ############# Calling the employees table an that fetches everything from their respective collections ###############
    # database_connection.employee_table(get_database_tables["employee"])
    # database_connection.login_table(get_database_tables["login"])
    # database_connection.role_table(get_database_tables["role"])

    app.run(port=5001, debug=True)