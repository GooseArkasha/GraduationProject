import os
from app import app, client, session
from models import *
import unittest
import tempfile
import json

class EmployeeTestCase(unittest.TestCase):
    data = [
        {
            'id': 0,
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'email': 'ivanov@mail.ru',
            'password': 'qwerty',
            'phone_number': '+7(968)-893-99-22'
        },
        {
            'id': 1,
            'first_name': 'Jack',
            'last_name': 'Black',
            'email': 'black@gmail.ru',
            'password': 'qwerty',
            'phone_number': '+7(968)-893-11-23'
        },
    ]
    def setUp(self):
        Employee.query.delete()
        for employee in self.data:
            new_emp = Employee(**employee)
            session.add(new_emp)
        session.commit()

    def test_get_employees_list(self):
        resp = client.get('/employees')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), len(self.data))
        self.assertEqual(resp.get_json()[0]['first_name'], self.data[0]['first_name'])

    def test_get_employee_correct_url(self):
        resp = client.get('/employees/0')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['first_name'], self.data[0]['first_name'])

    def test_get_employee_incorrect_url(self):
        resp = client.get('/employees/1000')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')

    def test_create_employee_correct_data(self):
        emp = {
            'id': 2,
            'first_name': 'Андрей',
            'last_name': 'Андреев',
            'patronymic': 'Андреевич',
            'email': 'andreev@mail.ru',
            'password': 'qwerty',
            'phone_number': '+7(968)-893-99-21'
        }

        resp = client.post('/employees', json=emp)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['first_name'], emp['first_name'])

    def test_update_employee_correct_url(self):
        replaced_info = {
            'email': 'ivanov@gmail.ru',
            'phone_number': '+7(968)-893-99-00'
        }

        resp = client.put('/employees/0', json=replaced_info)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['email'], replaced_info['email'])
        self.assertEqual(resp.get_json()['phone_number'], replaced_info['phone_number'])

    def test_update_employee_incorrect_url(self):
        replaced_info = {
            'email': 'ivanov@gmail.ru',
            'phone_number': '+7(968)-893-99-00'
        }

        resp = client.put('/employees/100', json=replaced_info)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')

    def test_delete_employee_correct_url(self):
        resp = client.delete('/employees/1')
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/employees/1')
        self.assertEqual(resp.status_code, 400)

    def test_delete_employee_incorrect_url(self):
        resp = client.delete('/employees/100')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')

if __name__ == '__main__':
    unittest.main()
