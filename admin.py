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
    employees = database_connection.merge_employee_role()
    return render_template("admin/admin.html", display_all_employees = employees, came_from = "admin.adminHome", search_result="")

@admin.route("/search", methods=["POST"])
def searchAnEmployee():
    print("Searvch: ", request.form.get('search_value'))
    fetch_search_result = request.form.get('search_value')
    fetch_names = database_connection.fetch_employee_search_name(fetch_search_result)
    print(fetch_names)
    if ( fetch_search_result ):
        return render_template("admin/admin.html", display_all_employees = fetch_names, search_result = fetch_search_result, value_search=request.form.get('search_value'))
    else:
        return redirect(url_for("admin.adminHome")) # If the search field is empty then navigate to the home page


@admin.route("/calendar")
def getFullCalendar():
    work_scheule = database_connection.workSchedule_table(work_schedle_db)
    print(work_scheule)
    events = work_scheule

    return render_template("admin/calendar.html", events = events)

# Drag the event from one date to the other date
@admin.route("/postData", methods=['GET', 'POST'])
def return_data():
    req_json_obj = request.json
    fetchedData = req_json_obj["eventData"]
    one_element = database_connection.fetch_only_one_work_schedule(fetchedData["_id"])
    print("one_element: ", one_element)
    print("fetchedData: ", fetchedData["end"])
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

    end_date_string = datetime.datetime.strptime(old_end_date,"%Y-%m-%dT%H:%M:%S")
    start_date_string = datetime.datetime.strptime(new_start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    new_format_end_time = "%H:%M:%S"
    new_format_start_time = "%Y-%m-%d"
    new_end_date = start_date_string.strftime(new_format_start_time) + 'T' + end_date_string.strftime(new_format_end_time)
    start_date_format = "%Y-%m-%dT%H:%M:%S"
    new_value_start = start_date_string.strftime(start_date_format)
    print("ONE ELEMENT: ", one_element)
    work_schedle_db.update_one(
        {'_id': one_element["_id"]},
        {'$set': { 'start': new_value_start , 'end': new_end_date}}
    )

    print(work_schedle_db.find_one({'_id': one_element["_id"]}))

    return jsonify(req_json_obj)