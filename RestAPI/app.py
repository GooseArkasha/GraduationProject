from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager, jwt_required
from config import Config
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import *
from flask_apispec import use_kwargs, marshal_with

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

docs = FlaskApiSpec()

docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='commercial_offers_creator',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})



from models import *

Base.metadata.create_all(bind=engine)

@app.route('/employees', methods=['GET'])
@jwt_required()
@marshal_with(EmployeeSchema(many=True))
def get_employees_list():
    employees = Employee.query.all()
    return employees

@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
@marshal_with(EmployeeSchema)
def get_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    return employee

@app.route('/employees', methods=['POST'])
@jwt_required()
@use_kwargs(EmployeeSchema)
@marshal_with(EmployeeSchema)
def create_employee(**kwargs):
    new_employee = Employee(**kwargs)
    session.add(new_employee)
    session.commit()
    return new_employee


@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(EmployeeSchema)
@marshal_with(EmployeeSchema)
def update_employee(employee_id, **kwargs):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    for key, value in kwargs.items():
        setattr(employee, key, value)
    session.commit()
    return employee

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
@marshal_with(EmployeeSchema)
def delete_employee(employee_id):
    employee = Employee.query.filter(Employee.id == employee_id).first()
    if not employee:
        return {'message': 'No Employees with this id'}, 400
    session.delete(employee)
    session.commit()
    return '', 204

@app.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    user = User(**kwargs)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def login(**kwargs):
    user = User.authenticate(**kwargs)
    token = user.get_token()
    return {'access_token': token}

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

docs.register(get_employees_list)
docs.register(get_employee)
docs.register(create_employee)
docs.register(update_employee)
docs.register(delete_employee)
docs.register(register)
docs.register(login)


if __name__ == '__main__':
    app.run()
