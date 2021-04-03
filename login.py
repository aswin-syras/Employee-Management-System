from flask import Blueprint, render_template, request, session, redirect, url_for, app

login = Blueprint("login", __name__, static_folder="static", template_folder="templates")

@login.route('/login_validation', methods=['GET', 'POST'])
def home():
    return User().login()
