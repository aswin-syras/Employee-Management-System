from datetime import datetime
from flask import Blueprint, render_template
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
from dateutil.relativedelta import relativedelta

department_db = database_connection.connect_department_table_name()
employee_type_db = database_connection.connect_employee_type_table_name()
all_roles = database_connection.connect_role_table_name()
gender_array = ['Not Ready to Declare', 'Male', 'Female']

employees = Blueprint("employees", __name__, static_folder="static", template_folder="templates")

class InformForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    startdate = DateField('Start Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    start_at = TimeField('Start at', format="'%h-%m'", validators=[DateRange(min=datetime.now())])
    end_at = TimeField('End at', format="'%h-%m'", validators=[DateRange(min=datetime.now())])
    date_of_joining = DateField('Date of Joining', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    date_of_birth = DateField('Date Of Birth', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    last_date = DateField('Last Date', format="%Y-%m-%d", )
    official_email_address = EmailField('Official Email address', validators=(validators.DataRequired(), validators.Email()))
    email_address = EmailField('Email address', validators=(validators.DataRequired(), validators.Email()))
    phoneNumber = StringField('Phone Number')
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
    current_address = StringField('Current Address')
    permanent_address = StringField('Permanent Address')
    is_active = BooleanField('Active')
    is_manager = BooleanField('Is a Manager?')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    hourly_pay = IntegerField('Hourly Pay')
    submit = SubmitField('Submit')

    department_name = StringField('Department Name', validators=[DataRequired()])
    employee_type_description = StringField('Employee Type Description', validators=[DataRequired()])

    role_name = StringField('Role Name', validators=[DataRequired()])
    role_have_full_power = BooleanField('Assign Full Power?')
    role_upload_documents_profile_pictures = BooleanField('Ablity to Upload Document?')

@employees.route("/")
# @employees.route("/<int:id>")
def home():
    # return render_template("employees/employee.html")
    # print()
    employees_one = database_connection.merge_employee_one_role(770301)
    print("-----: ", employees_one)
    for employee in employees_one:
        employee["date_of_joining"] = datetime.strptime(employee["date_of_joining"],
                                                                 '%Y-%m-%dT%H:%M%S').strftime("%B %d, %Y")

    return render_template("employees/employee-info.html", display_all_employees=employees_one, came_from="employees.home",
                           search_result="")


@employees.route("/editEmployee/<int:id>")
def editEmployee(id):
    # Fetch only the particular employee whose Id matches in the database
    dbdepartment=database_connection.department_table(department_db)
    dbemployee=database_connection.employee_type_table(employee_type_db)
    find_one = database_connection.fetch_only_one_employee(id)
    form = InformForm()
    twenty_yrs_ago = datetime.now() - relativedelta(years=20)
    strp_today = twenty_yrs_ago.strftime("%Y-%m-%d")
    print("strp_today: ", strp_today)

    print("***************** ", find_one)
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
    print(dbdepartment)
    fetch_all_departments = [doc for doc in dbdepartment]
    fetch_all_employee_type = [doc for doc in dbemployee]

    all_managers = database_connection.connect_manager_table_name()
    return render_template("shared-component/edit_employee.html",
                           form=form,
                           one_employee=find_one,
                           display_all_roles=database_connection.role_table(all_roles),
                           display_all_managers=database_connection.manager_table(all_managers),
                           display_all_departments=fetch_all_departments,
                           display_all_employee_type=fetch_all_employee_type,
                           came_from="admin.adminHome",
                           gender_array=gender_array,
                           twenty_yrs_ago=strp_today)

