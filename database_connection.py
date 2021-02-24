import pymongo

def database_connection () :
    connection_string = "mongodb+srv://Username:Password@cluster0.j1u4m.mongodb.net/EmployeeManagementSystem?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    database_name = my_client["EmployeeManagementSystem"]
    login_table_name = database_name["login"]
    employee_table_name = database_name["employees"]
    role_table_name = database_name["role"]

    return { "login": login_table_name, "employee": employee_table_name, "role": role_table_name }

def login_table (login):

    # print(all_collections)
    fetch_values = login.find()
    login_user = [record for record in fetch_values]
    print(login_user)

def employee_table(employee):
    # print(all_collections)
    fetch_values = employee.find()
    employee_user = [record for record in fetch_values]
    print(employee_user)


def role_table(role):
    # print(all_collections)
    fetch_values = role.find()
    role_user = [record for record in fetch_values]
    print(role_user)

def overall_connection ():
    all_collections = database_connection()
    return all_collections
# login_table(all_collections['login'])
# employees_table(all_collections['employee'])
# role_table(all_collections['role'])

