# pip install Flask

from flask import Flask, request, jsonify  
import repository
app = Flask(__name__)

# read all employees
@app.route("/employees",methods=['GET'])
def read_all():
    employees = repository.read_all()
    return jsonify(employees)
# create employee 
@app.route("/employees", methods=['POST'])
def create_employee():
    employee = request.get_json()
    repository.create_employee(employee['id'], employee['name'])
    return jsonify(employee)
# read by id 
@app.route("/employees/<id>",methods=['GET'])
def read_by_id(id):
    id = int(id)
    emp = repository.read_by_id(id)
    return jsonify(emp)
# update 
@app.route("/employees/<id>",methods=['PUT'])
def update(id):
    id = int(id)
    emp = request.get_json()
    repository.update(id,emp['name'])
    updatedEmp = repository.read_by_id(id)
    return jsonify(updatedEmp)
@app.route("/employees/<id>",methods=['DELETE'])
def delete_by_id(id):
    id = int(id)
    repository.delete_by_id(id)
    return jsonify()
# run the app 
app.run(debug=True)