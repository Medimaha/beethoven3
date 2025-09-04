
import logging 
import pickle
import os
from app_errors import CreateEmployeeException

logging.basicConfig(filename='app.log', 
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)

file_name = 'employee.dat'#dat means binary


def load_from_file():
    if os.path.exists(file_name):
        try:
          with open(file_name,'r')as reader:
           employees = pickle.load(reader)
        except Exception as ex:
           logging.error(ex)
           employees=[]
    else:
        employees = []
    return employees

def save_to_file(employees):
    try:
        with open(file_name,'wb') as writer:
           pickle.dump(employees, writer)
    except Exception as ex:
           logging.error(ex)
           raise CreateEmployeeException("Error in Employee creation.")


employees =load_from_file() #[]
def create_employee(id, name, job_title, salary, join_date):    
    emp = {
        'id':id, 
        'name': name, 
        'job_title': job_title, 
        'salary': salary, 
        'join_date': join_date
    }
    employees.append(emp)
    save_to_file(employees)
    logging.info(f'{name} Employee Created.')
def read_all():
    return employees
