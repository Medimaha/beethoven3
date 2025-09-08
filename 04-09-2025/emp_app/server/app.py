# pip install Flask

from flask import Flask, request, jsonify  
import repository
app = Flask(__name__)
repository.employeeTablesCreate()
# read all employees
@app.route("/employees",methods=['GET'])
def read_all():
    employees_objects = repository.readAllEmployees()
    employees = []
    for emp_obj in employees_objects:
        emp = {'id' : emp_obj.id, 'name': emp_obj.name}
        employees.append(emp)
    return jsonify(employees)
# create employee 
@app.route("/employees", methods=['POST'])
def create_employee():
    employee = request.get_json()
    id = repository.createEmployee(repository.Employee(name=employee['name']))
    emp_obj = repository.readEmployeeById(id)
    savedEmployee = {'id':emp_obj.id, 'name':emp_obj.name}
    return jsonify(savedEmployee)
# read by id 
@app.route("/employees/<id>",methods=['GET'])
def read_by_id(id):
    id = int(id)
    emp_obj = repository.readEmployeeById(id)
    employee = {'id':emp_obj.id, 'name':emp_obj.name}
    return jsonify(employee)
# update 
@app.route("/employees/<id>",methods=['PUT'])
def update(id):
    id = int(id)
    emp = request.get_json()
    repository.updateEmployee(repository.Employee(id,emp['name']))
    emp_obj = repository.readEmployeeById(id)
    savedEmployee = {'id':emp_obj.id, 'name':emp_obj.name}
    return jsonify(savedEmployee)
@app.route("/employees/<id>",methods=['DELETE'])
def delete_by_id(id):
    id = int(id)
    repository.deleteEmployee(id)
    return jsonify()
# run the app 
app.run(debug=True)