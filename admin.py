from flask import Blueprint, render_template, request, url_for, redirect, jsonify
import database_connection
import json
import datetime

import gridfs

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")
# Employee Table
fetch_all_employees_table = database_connection.connect_employee_table_name()
data_conn = database_connection.database_connection()
work_schedle_db = database_connection.connect_workSchedule_table_name()


@admin.route("/")
@admin.route("/home")
def adminHome():
    employees = database_connection.merge_employee_role('home')
    for employee in employees:
        employee["date_of_joining"]=datetime.datetime.strptime(employee["date_of_joining"], '%Y-%m-%dT%H:%M%S').strftime("%B %d, %Y")

    return render_template("admin/admin.html", display_all_employees=employees, came_from="admin.adminHome",
                           search_result="")

@admin.route("/search", methods=["POST"])
def searchAnEmployee():
    fetch_search_result = request.form.get('search_value')
    fetch_names = database_connection.fetch_employee_search_name(fetch_search_result)
    if (fetch_search_result):
        return render_template("admin/admin.html", display_all_employees=fetch_names, search_result=fetch_search_result,
                               value_search=request.form.get('search_value'))
    else:
        return redirect(url_for("admin.adminHome"))  # If the search field is empty then navigate to the home page


@admin.route("/calendar")
def getFullCalendar():
    work_scheule = database_connection.workSchedule_table(work_schedle_db)
    events = work_scheule

    return render_template("admin/calendar.html", events=events)

# Drag the event from one date to the other date
@admin.route("/postData", methods=['GET', 'POST'])
def return_data():
    req_json_obj = request.json
    fetchedData = req_json_obj["eventData"]
    one_element = database_connection.fetch_only_one_work_schedule(fetchedData["_id"])

    new_start_date = str(fetchedData["start"])
    old_end_date = fetchedData["end"]
    # datetimeobject = datetime.strptime(oldformat,'%Y%m%d')
    # print(dateFetched.year, dateFetched.month, dateFetched.day)
    # cur = oldformat.split('T')
    # end_time= old_end_date.split("T")
    # print(old_end_date.strftime("%H:%M:%S"))
    # year, month, day = cur[0].split("-")
    # today = datetime.date(int(year), int(month), int(day))
    # print(today)
    # print(end_time[1])

    end_date_string = datetime.datetime.strptime(old_end_date, "%Y-%m-%dT%H:%M")
    start_date_string = datetime.datetime.strptime(new_start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    new_format_end_time = "%H:%M:%S"
    new_format_start_time = "%Y-%m-%d"
    new_end_date = start_date_string.strftime(new_format_start_time) + 'T' + end_date_string.strftime(
        new_format_end_time)
    start_date_format = "%Y-%m-%dT%H:%M:%S"
    new_value_start = start_date_string.strftime(start_date_format)
    work_schedle_db.update_one(
        {'_id': one_element["_id"]},
        {'$set': {'start': new_value_start, 'end': new_end_date}}
    )
    return jsonify(req_json_obj)


@admin.route("/EmployeeActive/<status>", methods=['GET'])
def employee_active_data(status):
    if status == 'Inactive':
        is_active = False
    elif status == 'active':
        is_active = True
    else:
        return redirect(url_for('admin.adminHome'))
    is_active_status = database_connection.fetch_active_inactive_employee(is_active)
    employees = database_connection.merge_employee_role(is_active_status) # Merging 3 tables
    for employee in employees:
        employee["date_of_joining"]=datetime.datetime.strptime(employee["date_of_joining"], '%Y-%m-%dT%H:%M%S').strftime("%B %d, %Y")
    print("is_active_status: ", is_active_status)
    return render_template("admin/admin.html", display_all_employees=employees, came_from="admin.adminHome",
                           search_result="", status=status)


@admin.route("/EditEmployee/event/<int:empId>")
def getEditEmployeeEventCalendar(empId):
    # events = database_connection.fetch_only_one_employee(empId)
    events = database_connection.fetch_work_schedule_particular_emp(empId)
    print("123: ", events)
    # print("Workshec: ", work_schedule_employee)
    # database_connection.fetch_only_one_work_schedule(id)
    # work_scheule = database_connection.workSchedule_table(work_schedle_db)
    # events = work_scheule
    #
    return render_template("shared-component/employee_calendar.html", employee_id=empId, events=events)
