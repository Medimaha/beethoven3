from salary_manager import create_salary,read_all,read_by_salary
from salary_manager import salaries,update,delete_by_salary

def menu():
    message='''
     1-Create Salary
     2-Read By Salaries
     3-Read By Salary
     4-Update
     5-Delete
     6-Exit/Logout
    '''
    choice = int(input(message))
    if choice == 1:
        salary=int(input('salary:'))
        create_salary(salary)
    elif choice==2:
          result_salaries=read_all()
          print('salaries:')
          for salary in result_salaries:
             print(salary)
    elif choice ==3:
        salary = int(input('search salary'))
        index=read_by_salary(salary)
        if salary == -1:
           print('salary is not found')
        else:
           print(f' Salary is at index{index}')
    elif choice ==4:
        old_salary=int(input('salary to update:'))
        new_salary=int(input('New Salary'))
        update(old_salary,new_salary)

    elif choice == 5:
         salary=int(input('salary to delete:'))
         delete_by_salary(salary)

    elif choice==6:
       print("Exit/Logout")

    return choice
   

def menus():
    print("Salary Management App")
    choice=menu()
    while choice!=6:
        choice=menu()
    print("Thank yo for using App")


menus()
