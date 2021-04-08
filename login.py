from flask import Blueprint, render_template, request, session, redirect, url_for, app
from datetime import datetime
from flask import Flask, request, render_template, url_for, session, redirect, flash
from flask_pymongo import PyMongo
import database_connection
import json
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import DateTimeLocalField, EmailField
import logging
from random import randrange


login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

# Login table name
login_table_name = database_connection.connect_login_table()


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = EmailField('Email Address', validators=(validators.DataRequired(), validators.Email()))
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


def generating_random_id_login():
    # Generating a new random id for employees
    i = 1
    all_login_info = database_connection.login_table(login_table_name)
    while (i > 0):
        random_id_generator = randrange(1, 1000000)

        # Fetch only the Id only for comparing
        result = map(lambda x: x["_id"], all_login_info)
        not_in_list = random_id_generator not in list(result)
        if (not_in_list):
            i = 0
            return random_id_generator
        else:
            i = 1

@login.route("/")
def login_info():
    form = LoginForm()
    return render_template("shared-component/login.html",
                           form1=form)


@login.route("/register")
def register():
    form = LoginForm()
    return render_template("shared-component/RegistrationForm.html",
                           form1=form)

@login.route("/signupPOST", methods=["GET","POST"])
def signupPostData():
    error = []
    if request.form.get('password') != request.form.get('confirm'):
        form = LoginForm()
        error.append("Password doesn't match")
        logging.critical("Password doesn't match")
        return render_template("shared-component/RegistrationForm.html",
                               error=error,
                               form1=form)
    else:
        insert_data = {
            "_id": generating_random_id_login(),
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "remember_me": request.form.get('remember'),
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "email_address": request.form.get('email')
        }

        login_table_name.insert_one(insert_data)
        logging.warning("Successfully Inserted")
        print(request.form)
        return redirect(url_for('login.login_info'))

def loginComparison ( all_login_info ):
    count = 1
    index = 0
    boolValue = False
    print(request.form)
    while count > 0:
        if index < len(all_login_info):
            if all_login_info[index]["username"] != request.form.get('username') and all_login_info[index]["password"] != request.form.get('password'):
                count += 1
                boolValue = False
            else:   # SUCCESS
                count = 0
                boolValue = True
                return boolValue
            index += 1

        else:
            count = 0



@login.route("/login_validation", methods=["POST"])
def login_validationPost():
    # Fetch all the data from the Login Collection
    all_login_info = database_connection.login_table(login_table_name)
    login_check = loginComparison(all_login_info)

    error = []
    if login_check:
        return "Success"
    else:
        error.append("Username and password doesn't match")
        form=LoginForm()
        return render_template("shared-component/login.html",
                               form1=form,
                               error=error)






