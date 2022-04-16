from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required
from config import Config

# App initialization

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)

@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees_list():
    employees = Employee.query.all()
    serialized = []
    for employee in employees:
        serialized.append({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'patronymic': employee.patronymic,
            'phone_number': employee.phone_number,
            'user_id': employee.user_id
        })
    return jsonify(serialized)

@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    serialized = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'patronymic': employee.patronymic,
        'phone_number': employee.phone_number,
        'user_id': employee.user_id
    }
    return jsonify(serialized)

@app.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    new_employee = Employee(**request.json)
    session.add(new_employee)
    session.commit()
    serialized = {
        'id': new_employee.id,
        'first_name': new_employee.first_name,
        'last_name': new_employee.last_name,
        'patronymic': new_employee.patronymic,
        'phone_number': new_employee.phone_number,
        'user_id': new_employee.user_id
    }
    return jsonify(serialized)


@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    params = request.json
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    for key, value in params.items():
        setattr(employee, key, value)
    session.commit()
    serialized = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'patronymic': employee.patronymic,
        'phone_number': employee.phone_number,
        'user_id': employee.user_id
    }
    return jsonify(serialized)

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    session.delete(employee)
    session.commit()
    return '', 204

@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
