from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# App initialization

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

@app.route('/employees', methods=['GET'])
def get_employees_list():
    employees = Employee.query.all()
    serialized = []
    for employee in employees:
        serialized.append({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name
        })
    return jsonify(serialized)

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not item:
        return {'message': 'No Employees with this id'}, 400
    serialized = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name
    }
    return jsonify(serialized)

@app.route('/employees', methods=['POST'])
def create_employee():
    new_employee = Employee(**request.json)
    session.add(new_employee)
    session.commit()
    serialized = {
        'id': new_employee.id,
        'first_name': new_employee.first_name,
        'last_name': new_employee.last_name
    }
    return jsonify(serialized)


@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    params = request.json
    if not item:
        return {'message': 'No Employees with this id'}, 400
    for key, value im params.items():
        setattr(employee, key, value)
    session.commit()
    serialized = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name
    }
    return jsonify(serialized)

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not item:
        return {'message': 'No Employees with this id'}, 400
    session.delete(employee)
    session.commit()
    return '', 204

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
