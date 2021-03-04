import pymongo

# ***************************Database Connection ********************************* #
def database_connection () :
    connection_string = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    database_name = my_client["EmployeeManagementSystem"]
    return database_name

#Connect the table only to login
def connect_login_table():
     database_name = database_connection()
     login_table_name = database_name["login"]
     return login_table_name

#Connect the table only to employees
def connect_employee_table_name():
    database_name = database_connection()
    employee_table_name = database_name["employees"]
    return employee_table_name

#Connect the table only to role
def connect_role_table_name():
    database_name = database_connection()
    role_table_name = database_name["role"]
    return role_table_name

#Connect the table only to role
def connect_manager_table_name():
    database_name = database_connection()
    managers_table_name = database_name["managers"]
    return managers_table_name

def connect_employees_role_table ():
    database_name = database_connection()
    employee_table_name = database_name["employees"]
    role_table_name = database_name["role"]
    return { "employee": employee_table_name, "role": role_table_name }

#Fetching all the table names to make life easier
def fetch_all_tables():
    database_name = database_connection()
    login_table_name = database_name["login"]
    employee_table_name = database_name["employees"]
    role_table_name = database_name["role"]
    manager_table_name = database_name["managers "]

    return { "login": login_table_name, "employee": employee_table_name, "role": role_table_name, 'manager': manager_table_name }

def merge_employee_role ():
    emp_role = connect_employees_role_table()
    emp = employee_table(emp_role["employee"])
    role = role_table(emp_role["role"])

    merged_array = []
    for employee in emp:
        for rol in role:
            if ( employee["user_role_id"] == rol["_id"] ) :
                employee["role"] = rol["role_name"]
                employee["department"] = rol["department"]
                merged_array.append(employee)
    return merged_array

def login_table (login):
    fetch_values = login.find()
    login_user = [record for record in fetch_values]
    return login_user

def employee_table(employee):
    fetch_values = employee.find()
    employee_user = [record for record in fetch_values]
    return employee_user


def role_table(role):
    fetch_values = role.find()
    role_user = [record for record in fetch_values]
    return role_user

def manager_table(manager):
    fetch_values = manager.find()
    manager_user = [record for record in fetch_values]
    return manager_user

def fetch_only_one_employee(id):
    fetch_one = connect_employee_table_name()
    query = { '_id' : id }
    find_one_employee = fetch_one.find_one(query)
    return find_one_employee

def vai():
    return()