import unittest
from emp.repo import create_employee, read_all

class CreateEmployeeTest(unittest.TestCase):
    def test_div_create(self):
        create_employee(1001, 'Divya Kumar', 'Business Analyst', 38000, '20-Aug-2025')
        employees = read_all()
        self.assertEqual(employees[0]['name'], 'Divya Kumar')
    def test_gowtham_create(self):
        create_employee(1002, 'Gowtham', 'Data Analyst', 50000, '22-Aug-2025')
        employees = read_all()
        self.assertEqual(employees[1]['name'], 'Gowtham')