from flask import Blueprint, render_template, request, url_for
import database_connection
import gridfs

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

# Employee Table
fetch_all_employees_table = database_connection.connect_employee_table_name()
data_conn = database_connection.database_connection()


@admin.route("/")
@admin.route("/home")
def adminHome():
    employees = database_connection.merge_employee_role()
    return render_template("admin/admin.html", display_all_employees = employees, came_from = "admin.adminHome")




