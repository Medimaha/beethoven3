employees = []
def create_employee(id, name):    
    emp = {'id':id, 'name': name}
    employees.append(emp)    
def read_all():
    return employees
def read_by_id(id):
    for emp in employees:
        if emp['id'] == id:
            return emp 
    return None 
def update(id, name):
    old_emp = read_by_id(id)
    old_emp['name'] = name 
def delete_by_id(id):
    emp = read_by_id(id)
    employees.remove(emp)