# pip install Flask

from flask import Flask, request, jsonify  
import repo
app = Flask(__name__)

# read all employees
@app.route("/employees",methods=['GET'])
def read_all():
    employees = repo.read_all()
    return jsonify(employees)
# create employee 
@app.route("/employees", methods=['POST'])
def create_employee():
    employee = request.get_json()
    repo.create_employee(employee['id'], employee['name'])
    return jsonify(employee)
# read by id 
@app.route("/employees/<id>",methods=['GET'])
def read_by_id(id):
    id = int(id)
    emp = repo.read_by_id(id)
    return jsonify(emp)
# update 
@app.route("/employees/<id>",methods=['PUT'])
def update(id):
    id = int(id)
    emp = request.get_json()
    repo.update(id,emp['name'])
    updatedEmp = repo.read_by_id(id)
    return jsonify(updatedEmp)
@app.route("/employees/<id>",methods=['DELETE'])
def delete_by_id(id):
    id = int(id)
    repo.delete_by_id(id)
    return jsonify()
# run the app 
app.run(debug=True)