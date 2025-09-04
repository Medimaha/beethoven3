'''
employees = [
    {'id':1001, 'name': 'Divya Kumar', 'job_title':'Business Analyst', 'salary': 38000, 'join_date': '20-Aug-2025'},
    {'id':1002, 'name': 'Gowtham', 'job_title':'Data Analyst', 'salary': 50000, 'join_date': '22-Aug-2025'},
    {'id':1003, 'name': 'Mohammed Mazhar', 'job_title':'Business Analyst', 'salary': 40000, 'join_date': '12-Aug-2025'},
    {'id':1004, 'name': 'Ovisha', 'job_title':'Data Analyst', 'salary': 51000, 'join_date': '25-Aug-2025'},
    {'id':1005, 'name': 'Udit', 'job_title':'Consulting Engineer', 'salary': 100000, 'join_date': '23-Aug-2025'},
    {'id':1006, 'name': 'Shrawan', 'job_title':'Software Engineer', 'salary': 200000, 'join_date': '08-Aug-2025'}
]

total = 0 
for employee in employees: 
    total += employee['salary']
print(total)
'''

from repo_pickle import create_employee, read_all
create_employee(1001, 'Divya Kumar', 'Business Analyst', 38000, '20-Aug-2025')
create_employee(1002, 'Gowtham', 'Data Analyst', 50000, '22-Aug-2025')
create_employee(1003, 'Mohammed Mazha', 'Business Analyst', 40000, '12-Aug-2025')

print(read_all())