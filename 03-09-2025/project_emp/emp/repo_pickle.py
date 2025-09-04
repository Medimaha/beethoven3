
import logging 
import pickle
import os

logging.basicConfig(filename='app.log', 
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO)

file_name = 'employee.dat'#dat means binary


def load_from_file():
    if os.path.exists(file_name):
        with open(file_name,'r')as reader:
           employees = pickle.load(reader)
    else:
        employees = []
    return employees

def save_to_file(employees):
    with open(file_name,'wb') as writer:
        pickle.dump(employees, writer)
    pass



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
