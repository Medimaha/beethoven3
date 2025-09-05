import sqlite3

def connect():
    con = sqlite3.connect('employee_app_db.db')
    return con 
def employeeTablesCreate():
    sql = """CREATE TABLE IF NOT EXISTS employee(
        id integer primary key AUTOINCREMENT,
        name varchar(255) not null
    )"""
    con = connect()
    con.execute(sql)
    con.close()
    print("Database is connected and in sync.")

class Employee:
    def __init__(self, id=None,
        name='',
        ratings=1,
        place='',
        phone_number=''):
        self.id = id 
        self.name = name 
    #def __str__(self):
    #    return f'[{self.id},{self.name}]'

def createEmployee(employee):
    sql = """INSERT INTO employee(name)
    VALUES(?)"""
    params = (employee.name,)
    con = connect()
    cur = con.cursor()
    cur.execute(sql,params)
    id = cur.lastrowid  #
    con.commit()
    con.close()
    return id           #

def readAllEmployees():
    sql = """SELECT id,name FROM employee"""
    params = tuple()
    con = connect()
    cur = con.cursor()
    response = cur.execute(sql,params)
    result = response.fetchall() #[rows], each row=[id,name,...]
    con.close()

    employees = []
    for row in result:
        employees.append(Employee(id=row[0],name=row[1]))
    return employees 

def updateEmployee(employee):
    sql = """UPDATE employee
    set name=?
    WHERE (id=?)"""
    params = (employee.name, employee.id, )
    con = connect()
    cur = con.cursor()
    cur.execute(sql,params)
    con.commit()
    con.close()

def deleteEmployee(id):
    sql = """DELETE from employee
    WHERE (id=?)"""
    params = (id, )
    con = connect()
    cur = con.cursor()
    cur.execute(sql,params)
    con.commit()
    con.close()
    
def readEmployeeById(id):
    sql = """SELECT id,name FROM employee
    WHERE (id=?)"""
    params = (id,)
    con = connect()
    cur = con.cursor()
    response = cur.execute(sql,params)
    result = response.fetchone() #row=[id,name,...]
    con.close()

    if result != None:
        employee = Employee(id=result[0],name=result[1])
    else:
        employee = None 
    return employee