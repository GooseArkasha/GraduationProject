import os
from app import app, client, session
from models import *
import unittest
import tempfile
import json


class UserTestCase(unittest.TestCase):
    data = [
        {
            'email': 'ivanov@mail.ru',
            'password': 'qwerty'
        },
        {
            'email': 'black@gmail.com',
            'password': 'password'
        }
    ]
    def setUp(self):
        User.query.delete()
        for user in self.data:
            new_user = User(**user)
            session.add(new_user)
        session.commit()
        session.remove()

    def test_register(self):
        user = {
            'email': 'andreev@gmail.com',
            'password': '123'
        }
        resp = client.post('/register', json=user)
        self.assertEqual(resp.status_code, 200)

    def test_ligin(self):
        resp = client.post('/login', json=self.data[0])
        self.assertEqual(resp.status_code, 200)


class EmployeeTestCase(unittest.TestCase):
    data = [
        {
            'id': 0,
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
            'phone_number': '+7(968)-893-99-22',
            'user_id':0
        },
        {
            'id': 1,
            'first_name': 'Jack',
            'last_name': 'Black',
            'phone_number': '+7(968)-893-11-23',
            'user_id':1
        },
    ]

    params = {
        'email': 'ivanov@mail.ru',
        'password': 'qwerty'
    }

    token = None

    def setUp(self):
        Employee.query.delete()
        for employee in self.data:
            new_emp = Employee(**employee)
            session.add(new_emp)

        User.query.delete()
        resp = client.post('/register', json=self.params)
        resp = client.post('/login', json=self.params)
        self.token = resp.get_json()['access_token']
        session.commit()
        session.remove()


    def test_get_employees_list(self):
        resp = client.get('/employees', headers={'Authorization': self.token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), len(self.data))
        self.assertEqual(resp.get_json()[0]['first_name'], self.data[0]['first_name'])

    def test_get_employee_correct_url(self):
        resp = client.get('/employees/0', headers={'Authorization': self.token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['first_name'], self.data[0]['first_name'])

    def test_get_employee_incorrect_url(self):
        resp = client.get('/employees/1000', headers={'Authorization': self.token})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')

    def test_create_employee_correct_data(self):
        emp = {
            'id': 2,
            'first_name': 'Андрей',
            'last_name': 'Андреев',
            'patronymic': 'Андреевич',
            'phone_number': '+7(968)-893-99-21',
            'user_id':2
        }

        resp = client.post('/employees', headers={'Authorization': self.token}, json=emp)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['first_name'], emp['first_name'])

    def test_update_employee_correct_urlnew_(self):
        replaced_info = {
            'phone_number': '+7(968)-893-99-00'
        }

        resp = client.put('/employees/0', headers={'Authorization': self.token}, json=replaced_info)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['phone_number'], replaced_info['phone_number'])

    def test_update_employee_incorrect_url(self):
        replaced_info = {
            'phone_number': '+7(968)-893-99-00'
        }

        resp = client.put('/employees/100', headers={'Authorization': self.token}, json=replaced_info)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')

    def test_delete_employee_correct_url(self):
        resp = client.delete('/employees/1', headers={'Authorization': self.token})
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/employees/1')
        self.assertEqual(resp.status_code, 400)

    def test_delete_employee_incorrect_url(self):
        resp = client.delete('/employees/100', headers={'Authorization': self.token})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['message'], 'No Employees with this id')


if __name__ == '__main__':
    unittest.main()
