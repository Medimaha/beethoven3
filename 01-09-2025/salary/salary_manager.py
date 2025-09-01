salaries=[]
#crud create,read all,read by id,delete,read by salary

def create_salary(salary):
    global salaries
    salaries.append(salary)

def read_all():
    return salaries

def read_by_salary(salary):       
    for I in range(len(salaries)):  
        if salaries[I]==salary :
            return I
    return -1

def update(old_salary,new_salary):
    global salaries
    index=read_by_salary(old_salary)
    salaries[index]=new_salary

def delete_by_salary(salary):
    index=read_by_salary(salary)
    salaries.pop(index)