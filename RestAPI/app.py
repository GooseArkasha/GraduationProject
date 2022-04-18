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
import logging


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

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

@app.route('/employees', methods=['GET'])
@jwt_required()
@marshal_with(EmployeeSchema(many=True))
def get_employees_list():
    try:
        employees = Employee.get_employees_list()
    except Exeption as e:
        logger.warning(f'read action faild with errors: {e}')
        return {'message': str(e)}, 400
    return employees

@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
@marshal_with(EmployeeSchema)
def get_employee(employee_id):
    try:
        employee = Employee.get_employee(employee_id)
        if not employee:
            return {'message': 'No Employees with this id'}, 400
    except Exception as e:
        logger.warning(f'read action faild with errors: {e}')
        return {'message': str(e)}, 400
    return employee

@app.route('/employees', methods=['POST'])
@jwt_required()
@use_kwargs(EmployeeSchema)
@marshal_with(EmployeeSchema)
def create_employee(**kwargs):
    try:
        new_employee = Employee(**kwargs)
        new_employee.save()
    except Exception as e:
        logger.warning(f'create action faild with errors: {e}')
        return {'message': str(e)}, 400
    return new_employee

@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(EmployeeSchema)
@marshal_with(EmployeeSchema)
def update_employee(employee_id, **kwargs):
    try:
        employee = Employee.get_employee(employee_id)
        employee.update(**kwargs)
    except Exception as e:
        logger.warning(f'update action faild with errors: {e}')
        return {'message': str(e)}, 400
    return employee

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
@marshal_with(EmployeeSchema)
def delete_employee(employee_id):
    try:
        employee = Employee.get_employee(employee_id)
        employee.delete()
    except Exception as e:
        logger.warning(f'delete action faild with errors: {e}')
        return {'message': str(e)}, 400
    return '', 204

@app.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        user.save()
        token = user.get_token()
    except Exception as e:
        logger.warning(f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': token}

@app.route('/login', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
    except Exception as e:
        logger.warning(
            f'login with email {kwargs["email"]} failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

@app.errorhandler(422)
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid Request.'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400

docs.register(get_employees_list)
docs.register(get_employee)
docs.register(create_employee)
docs.register(update_employee)
docs.register(delete_employee)
docs.register(register)
docs.register(login)


if __name__ == '__main__':
    app.run()
