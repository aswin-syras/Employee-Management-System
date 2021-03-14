# import pymongo
from datetime import datetime

from flask import Flask, request, render_template, url_for, session, redirect, flash
from login import login
from admin import admin
from employees import employees
from flask_pymongo import PyMongo
import database_connection
import json
from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, required, NumberRange, Optional
from wtforms import validators, SubmitField, StringField
from wtforms.fields.html5 import DateTimeLocalField, EmailField
from wtforms_components import DateRange
from bson import ObjectId
from random import randrange
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

app = Flask(__name__)
app.config['SECRET_KEY'] = "$%^&U$%^TYURTFY&*GU"

###### BluePrint for differernt pages
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(employees, url_prefix="/employees")

app.config[
    "MONGO_URI"] = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
mongo = PyMongo(app)

fetch_database_connection = database_connection.database_connection()

#### Fetch only certain table
all_roles = database_connection.connect_role_table_name()
all_managers = database_connection.connect_manager_table_name()
all_employees = database_connection.connect_employee_table_name()
fetch_all_employee_type = [doc for doc in mongo.db.employee_type.find()]
fetch_all_departments = [doc for doc in mongo.db.departments.find()]

print("Employee type", fetch_all_employee_type)
print("Department type", fetch_all_departments)

# all_work_schedule = database_connection.connect_workSchedule_table_name()


gender_array = ['Not Ready to Declare', 'Male', 'Female']


# mongo.db.employees.delete_many({})
# mongo.db.managers.delete_many({})
# mongo.db.role.delete_many({})


class InformForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    startdate = DateField('Start Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    start_at = TimeField('Start at', format="'%h-%m'", validators=[DateRange(min=datetime.now())])
    end_at = TimeField('End at', format="'%h-%m'", validators=[DateRange(min=datetime.now())])
    date_of_joining = DateField('Date of Joining', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    date_of_birth = DateField('Date Of Birth', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    last_date = DateField('Last Date', format="%Y-%m-%d", )
    official_email_address = EmailField('Official Email address', [validators.DataRequired(), validators.Email()])
    email_address = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    salary = h5fields.IntegerField(
        "Salary", widget=h5widgets.NumberInput(min=0)
    )
    bonus = h5fields.IntegerField(
        "Bonus", widget=h5widgets.NumberInput(min=0)
    )
    bank_name = StringField('Bank Name')
    account_number = StringField('Account Number')
    UAN_number = StringField('UAN Number')
    basic_allowance = h5fields.IntegerField(
        "Basic Allowance", widget=h5widgets.NumberInput(min=0)
    )
    medical_allowance = h5fields.IntegerField(
        "Medical Allowance", widget=h5widgets.NumberInput(min=0)
    )
    provident_fund = h5fields.IntegerField(
        "Provident Fund", widget=h5widgets.NumberInput(min=0)
    )
    tax = h5fields.IntegerField(
        "Tax", widget=h5widgets.NumberInput(min=0)
    )
    current_address = TextAreaField('Current Address')
    permanent_address = TextAreaField('Permanent Address')
    is_active = BooleanField('Active')
    is_manager = BooleanField('Is a Manager?')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    hourly_pay = IntegerField('Hourly Pay')
    submit = SubmitField('Submit')


@app.route("/<name>")
def home(name):
    return render_template("shared-component/index.html", content=name)


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


def generating_random_id_employees():
    # Generating a new random id for employees
    i = 1
    while (i > 0):
        random_id_generator = randrange(1, 1000000)
        all_employees_find = mongo.db.employees.find()

        # Fetch only the Id only for comparing
        result = map(lambda x: x["_id"], all_employees_find)
        not_in_list = random_id_generator not in list(result)
        if (not_in_list):
            i = 0
            return random_id_generator
        else:
            i = 1


@app.route("/newEmployee")
def createNewEmployeeGET():
    # all_roles = database_connection.connect_role_table_name()
    # all_managers = database_connection.connect_manager_table_name()
    form = InformForm()

    return render_template("shared-component/new_employee.html",
                           display_all_roles=database_connection.role_table(all_roles),
                           display_all_managers=database_connection.manager_table(all_managers),
                           display_all_departments=fetch_all_departments,
                           display_all_employee_type=fetch_all_employee_type,
                           form=form,
                           came_from="admin.adminHome",
                           gender_array=gender_array)


@app.route("/createNewEmployee", methods=['POST'])
def createNewEmployee():
    if "profile_image" in request.files:
        profile_image = request.files["profile_image"]
        mongo.save_file(profile_image.filename, profile_image)
        all_employees_table = database_connection.connect_employee_table_name()
        all_emp_record = database_connection.employee_table(all_employees_table)

        print(request.form)
        requestForm = {}
        form = InformForm()

        if (not request.form.get("employee_type_id") or not request.form.get("manager_id") or not request.form.get(
                "role_id") or not request.form.get("department_id")):

            error = []

            print("request.form.get:::", request.form.get("manager_id"), request.form )
            if not request.form.get("role_id"):
                error.append("Please Select the Job Position")
            elif request.form.get("role_id"):
                requestForm.update({'role_id': int(request.form.get("role_id"))})

            if not request.form.get("manager_id"):
                error.append("Please Select the Reporting Manager")
            elif request.form.get("manager_id"):
                requestForm.update({'manager_id': int(request.form.get("manager_id"))})

            if not request.form.get("employee_type_id"):
                error.append("Please Select the Employment Type")
            elif request.form.get("employee_type_id"):
                requestForm.update({'employee_type_id': int(request.form.get("employee_type_id"))})

            if not request.form.get("department_id"):
                error.append("Please Select the Department")
            elif request.form.get("department_id"):
                requestForm.update({'department_id': int(request.form.get("department_id"))})

            return render_template("shared-component/new_employee.html",
                                   display_all_roles=database_connection.role_table(all_roles),
                                   display_all_managers=database_connection.manager_table(all_managers),
                                   display_all_departments=fetch_all_departments,
                                   display_all_employee_type=fetch_all_employee_type,
                                   form=form,
                                   error=error,
                                   came_from="admin.adminHome",
                                   gender_array=gender_array,
                                   requestForm=requestForm)
        elif int(request.form.get("employee_type_id")) != 1000 and request.form.get("is_manager"): # If manager cannot be in Hourly rate
            error = []
            error.append("Manager Cannot be on an hourly rate")
            requestForm.update({'role_id': int(request.form.get("role_id"))})
            requestForm.update({'manager_id': int(request.form.get("manager_id"))})
            requestForm.update({'employee_type_id': int(request.form.get("employee_type_id"))})
            requestForm.update({'department_id': int(request.form.get("department_id"))})

            return render_template("shared-component/new_employee.html",
                                   display_all_roles=database_connection.role_table(all_roles),
                                   display_all_managers=database_connection.manager_table(all_managers),
                                   display_all_departments=fetch_all_departments,
                                   display_all_employee_type=fetch_all_employee_type,
                                   form=form,
                                   error=error,
                                   came_from="admin.adminHome",
                                   gender_array=gender_array,
                                   requestForm=requestForm)
        else:
            salary_hourly_details = {}
            print("--------------------: ", int(request.form.get("employee_type_id")) , request.form.get("is_manager"))
            # Fulltime job has some benefits
            if (int(request.form.get('employee_type_id')) == 1000):
                my_salary = request.form.get('salary')
                my_bonus = request.form.get('bonus')
                my_basic_allowance = request.form.get('basic_allowance')
                my_medical_allowance = request.form.get('medical_allowance')
                my_provident_fund = request.form.get('provident_fund')
                my_tax = request.form.get('tax')

                salary_hourly_details = {
                    "salary_details": {
                        "salary": 0 if not my_salary else float(request.form.get('salary')),
                        "bonus": 0 if not my_bonus else float(request.form.get('bonus')),
                        "allowances": {
                            "basic_allowance": 0 if not my_basic_allowance else float(request.form.get('basic_allowance')),
                            "medical_allowance": 0 if not my_medical_allowance else float(request.form.get('medical_allowance')),
                            "provident_fund": 0 if not my_provident_fund else float(request.form.get('provident_fund')),
                            "tax": 0 if not my_tax else float(request.form.get('tax'))
                        }
                    }
                }
            else:
                myhourly_pay = request.form.get('hourly_pay')
                salary_hourly_details = {
                    "hourly_pay_details": {
                        "hourly_pay": 0 if not myhourly_pay else float(request.form.get('hourly_pay'))
                    }
                }

            insert_data = {
                '_id': generating_random_id_employees(),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'phone_number': request.form.get('phoneNumber'),
                'email_address': request.form.get('email_address'),
                'user_role_id': int(request.form.get('role_id')),
                'user_manager_id': int(request.form.get('manager_id')),
                'gender': request.form.get('gender'),
                'profile_image_name': profile_image.filename,
                'is_active': True if request.form.get('is_active') else False,
                'employee_type_id': int(request.form.get('employee_type_id')),
                'department_id': int(request.form.get('department_id')),
                'date_of_birth': request.form.get('date_of_birth'),
                'date_of_joining': request.form.get('date_of_joining'),
                'last_date': request.form.get('last_date'),
                'official_email_address': request.form.get('official_email_address'),
                'is_manager': True if request.form.get('is_manager') else False,
                'bank_details': {
                    'bank_name': request.form.get('bank_name'),
                    'account_number': request.form.get('account_number'),
                    'UAN_number': request.form.get('UAN_number'),
                },
                'address': {
                    'current_address': request.form.get('current_address'),
                    'permanent_address': request.form.get('permanent_address')
                }
            }

            insert_data.update(salary_hourly_details)

            # If the is a Manager? then insert the user into the table
            if (request.form.get('is_manager')):
                manager_data = {
                      "_id": insert_data["_id"],
                      "manager_first_name": insert_data["first_name"],
                      "manager_last_name": insert_data["last_name"],
                      "manager_role_id": insert_data['user_role_id'],
                      "manager_department_id": insert_data["department_id"]
                }
                mongo.db.managers.insert_one(manager_data)

            # Insert the employees  data into the employees collection
            mongo.db.employees.insert_one(insert_data)
        return redirect(url_for("admin.adminHome"))


@app.route("/editEmployee/<int:id>")
def editEmployee(id):
    # Fetch only the particular employee whose Id matches in the database
    find_one = database_connection.fetch_only_one_employee(id)
    form = InformForm()
    print("***************** ", 'hourly_pay_details' in find_one)
    one_salary_hourly_pay = {}
    if 'hourly_pay_details' in find_one:
        one_salary_hourly_pay = {
            'hourly_pay': find_one['hourly_pay_details']['hourly_pay']
        }
    else:
        one_salary_hourly_pay = {
            'salary': find_one['salary_details']['salary'],
            "bonus": find_one['salary_details']['bonus'],
            "basic_allowance": find_one['salary_details']['allowances']['basic_allowance'],
            "medical_allowance": find_one['salary_details']['allowances']['medical_allowance'],
            "provident_fund": find_one['salary_details']['allowances']['provident_fund'],
            "tax": find_one['salary_details']['allowances']['tax']
        }
    find_one.update(one_salary_hourly_pay)

    return render_template("shared-component/edit_employee.html",
                           form=form,
                           one_employee=find_one,
                           display_all_roles=database_connection.role_table(all_roles),
                           display_all_managers=database_connection.manager_table(all_managers),
                           display_all_departments=fetch_all_departments,
                           display_all_employee_type=fetch_all_employee_type,
                           came_from="admin.adminHome",
                           gender_array=gender_array)


@app.route("/editAnEmployee/<int:id>", methods=['POST'])
def editAnEmployee(id):
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
            'user_manager_id': int(request.form.get('manager_id')) if found_one_from_db_before_json[
                "user_manager_id"] else found_one_from_db_before_json["user_manager_id"],
            'gender': request.form.get('gender'),
            'profile_image_name': profile_image.filename if profile_image.filename else found_one_from_db_before_json[
                "profile_image_name"]
        }

        fetched_val_json = json.dumps(fetched_value_before_json, sort_keys=True)

        collect_data_to_append = {}
        if converted_json == fetched_val_json:
            print("They are Exactly the same, so don't update the db")
        else:
            if (fetched_value_before_json["first_name"] != found_one_from_db_before_json["first_name"]):
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
                {'_id': id},
                {'$set': collect_data_to_append}
            )

        # TODO: Need to redirect it to the desired location
        return redirect(url_for("admin.adminHome"))


# Delete an Event
@app.route("/deleteExistingEmployee/<int:id>")
def deleteExistingEmployee(id):
    print("ID: ", id, )
    fetch_one_employee = mongo.db.employees.find_one({ '_id': id })
    if fetch_one_employee['is_manager']:
        mongo.db.managers.delete_one({'_id': id})
    mongo.db.employees.delete_one({'_id': id})
    return redirect(url_for('admin.adminHome'))


# ********************************** CREATING CALENDAR EVENT *****************************#
@app.route("/createNewEventPost", methods=['GET', 'POST'])
def createNewEventPost():
    form = InformForm()
    # TODO we may need to show all the employees list
    print("NEW: ", request.form.get("employee_id"))

    # TODO remove this
    today = datetime.now()
    strp_today = today.strftime("%Y-%m-%d %H:%M")
    curr_date_time = datetime.strptime(strp_today, "%Y-%m-%d %H:%M")
    timestamp_current_date_time = datetime.timestamp(curr_date_time)

    print("NOW: ", timestamp_current_date_time)

    if (form.validate_on_submit()):
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        return redirect(url_for("date"))
    return render_template('admin/new_event_creation.html',
                           form=form,
                           display_all_employees=database_connection.employee_table(all_employees),
                           display_all_managers=database_connection.manager_table(all_managers))


@app.route("/admin/calendar", methods=['POST'])
def date():
    form = InformForm()
    session['startdate'] = form.startdate.data
    session['enddate'] = form.enddate.data
    startdate = session["startdate"]
    enddate = session["enddate"]

    # TODO Need to validate and some logics
    # https://www.dataquest.io/blog/python-datetime-tutorial/
    start_date_split = request.form.get('startdate').split("-")
    start_at_split = request.form.get('start_at').split(":")

    end_date_split = request.form.get('enddate').split("-")
    end_at_split = request.form.get('end_at').split(":")

    # date1 = datetime(int(start_date_split[0]), int(start_date_split[1]), int(start_date_split[2]), int(start_at_split[0]), int(start_at_split[1]), 00)
    # date2 = datetime(int(end_date_split[0]), int(end_date_split[1]), int(end_date_split[2]), int(end_at_split[0]), int(end_at_split[1]), 00)
    #
    # diff = date2 - date1
    # print("Difference: ", diff)

    print("NEW: ", request.form.get("employee_id"))
    print("FORM: ", request.form, datetime.now())

    requestForm = {
        "employee_id": int(request.form.get("employee_id")),
        "manager_id": int(request.form.get("manager_id"))
    }

    dt_object1 = datetime.strptime(request.form.get('startdate') + ' ' + request.form.get('start_at'), "%Y-%m-%d %H:%M")
    dt_object2 = datetime.strptime(request.form.get('enddate') + ' ' + request.form.get('end_at'), "%Y-%m-%d %H:%M")
    timestamp = datetime.timestamp(dt_object2)
    timestamp2 = datetime.timestamp(dt_object1)

    # Today's timestamp
    today = datetime.now()
    strp_today = today.strftime("%Y-%m-%d %H:%M")
    curr_date_time = datetime.strptime(strp_today, "%Y-%m-%d %H:%M")
    timestamp_current_date_time = datetime.timestamp(curr_date_time)

    today = datetime.now()
    print("NOW: ", float(timestamp_current_date_time) < float(timestamp))
    print("Float: ", float(timestamp_current_date_time), float(timestamp))

    error = None
    if (timestamp == timestamp2):
        print("They r same, please try something else")
        # flash("Start date and End date are same, please try to enter the start date to be less than the end date")
        error = 'Start date and End date are same, please try to enter the start date to be less than the end date'
        return render_template('admin/new_event_creation.html',
                               form=form,
                               display_all_employees=database_connection.employee_table(all_employees),
                               display_all_managers=database_connection.manager_table(all_managers), error=error,
                               requestForm=requestForm)

    elif (float(timestamp) < float(timestamp2)):
        print("Looks like the start date is greater than end date")
        error = 'Looks like the start date is greater than end date'
        return render_template('admin/new_event_creation.html',
                               form=form,
                               display_all_employees=database_connection.employee_table(all_employees),
                               display_all_managers=database_connection.manager_table(all_managers), error=error,
                               requestForm=requestForm)
    else:
        print("Looks like it is the correct date: ", request.form, session)
        mongo.db.workSchedule.insert_one({
            'employee_id': int(request.form.get('employee_id')),
            'title': request.form.get('title'),
            'start': request.form.get('startdate') + 'T' + request.form.get('start_at'),
            'end': request.form.get('enddate') + 'T' + request.form.get('end_at'),
            'manager_id': int(request.form.get('manager_id'))})
        return redirect(url_for("admin.getFullCalendar"))


@app.route("/getExistingEvent/<id>", methods=['GET', 'POST'])
def editExitEvent(id):
    one_element = database_connection.fetch_only_one_work_schedule(ObjectId(id))
    form = InformForm()
    # TODO we may need to show all the employees list

    return render_template('admin/edit_event_creation.html',
                           form=form,
                           display_all_employees=database_connection.employee_table(all_employees),
                           display_all_managers=database_connection.manager_table(all_managers),
                           fetched_data=one_element)


@app.route("/postAnExistingEvent/<id>", methods=['POST'])
def postAnExistingEventData(id):
    requestForm = {
        "employee_id": int(request.form.get("employee_id")),
        "manager_id": int(request.form.get("manager_id"))
    }
    form = InformForm()
    print("req: ", requestForm)
    #
    # print("request.form:::: ", request.form["startdate"], request.form.get('startdate'))
    value_date1 = request.form.get('startdate') + ' ' + request.form.get('start_at')
    print("+++++++++++++++++++++: ", value_date1)

    dt_object1 = datetime.strptime(request.form.get('startdate') + ' ' + request.form.get('start_at'), "%Y-%m-%d %H:%M")
    dt_object2 = datetime.strptime(request.form.get('enddate') + ' ' + request.form.get('end_at'), "%Y-%m-%d %H:%M")
    timestamp = datetime.timestamp(dt_object2)
    timestamp2 = datetime.timestamp(dt_object1)
    error = None

    print(dt_object1, dt_object2)
    print(timestamp, timestamp2)

    if (timestamp == timestamp2):
        print("******: ++++++++++ ", form)

        one_element = {
            "_id": ObjectId(id),
            "employee_id": int(request.form.get("employee_id")),
            "manager_id": int(request.form.get("manager_id")),
            "title": request.form.get("title"),
            'start': request.form.get('startdate') + 'T' + request.form.get('start_at'),
            'end': request.form.get('enddate') + 'T' + request.form.get('end_at'),
        }

        print("They r same, please try something else")
        # flash("Start date and End date are same, please try to enter the start date to be less than the end date")
        error = 'Start date and End date are same, please try to enter the start date to be less than the end date'
        return render_template('admin/edit_event_creation.html',
                               form=form,
                               display_all_employees=database_connection.employee_table(all_employees),
                               display_all_managers=database_connection.manager_table(all_managers),
                               error=error,
                               requestForm=requestForm,
                               fetched_data=one_element)
    elif (float(timestamp) < float(timestamp2)):
        one_element = {
            "_id": ObjectId(id),
            "employee_id": int(request.form.get("employee_id")),
            "manager_id": int(request.form.get("manager_id")),
            "title": request.form.get("title"),
            'start': request.form.get('startdate') + 'T' + request.form.get('start_at'),
            'end': request.form.get('enddate') + 'T' + request.form.get('end_at'),
        }
        print("Looks like the start date is greater than end date")
        error = 'Looks like the start date is greater than end date'
        return render_template('admin/edit_event_creation.html',
                               form=form,
                               display_all_employees=database_connection.employee_table(all_employees),
                               display_all_managers=database_connection.manager_table(all_managers),
                               error=error,
                               requestForm=requestForm,
                               fetched_data=one_element)

    else:
        found_one_from_db_before_json = database_connection.fetch_only_one_work_schedule(ObjectId(id))

        del found_one_from_db_before_json["_id"]
        converted_json = json.dumps(found_one_from_db_before_json, sort_keys=True)
        fetched_value_before_json = {
            'employee_id': int(request.form.get('employee_id')),
            'title': request.form.get('title'),
            'manager_id': int(request.form.get('manager_id')),
            'start': request.form.get('startdate') + 'T' + request.form.get('start_at'),
            'end': request.form.get('enddate') + 'T' + request.form.get('end_at'),
        }
        fetched_val_json = json.dumps(fetched_value_before_json, sort_keys=True)

        collect_data_to_append = {}
        if converted_json == fetched_val_json:
            print("They are Exactly the same, so don't update the db")
        else:
            if (fetched_value_before_json["employee_id"] != found_one_from_db_before_json["employee_id"]):
                collect_data_to_append["employee_id"] = fetched_value_before_json["employee_id"]
            if (fetched_value_before_json["title"] != found_one_from_db_before_json["title"]):
                collect_data_to_append["title"] = fetched_value_before_json["title"]
            if (fetched_value_before_json["manager_id"] != found_one_from_db_before_json["manager_id"]):
                collect_data_to_append["manager_id"] = fetched_value_before_json["manager_id"]
            if (fetched_value_before_json["start"] != found_one_from_db_before_json["start"]):
                collect_data_to_append["start"] = fetched_value_before_json["start"]
            if (fetched_value_before_json["end"] != found_one_from_db_before_json["end"]):
                collect_data_to_append["end"] = fetched_value_before_json["end"]

            mongo.db.workSchedule.update_one(
                {'_id': ObjectId(id)},
                {'$set': collect_data_to_append}
            )
        return redirect(url_for('admin.getFullCalendar'))


# Delete an Event
@app.route("/deleteEvent/<id>")
def deleteEvent(id):
    mongo.db.workSchedule.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('admin.getFullCalendar'))


if __name__ == '__main__':
    app.run(port=5001, debug=True)
