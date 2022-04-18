from app import db, session, Base
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import relationship
from datetime import timedelta
from passlib.hash import bcrypt

class Employee(Base):
    __tablename__= 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    patronymic =  db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    phone_number = db.Column(db.String(250), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #position_id = db.Column(db.Integer, FoForeignKey(positions.id)

    @classmethod
    def get_employees_list(cls):
        try:
            employees = cls.query.all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return employees

    @classmethod
    def get_employee(cls, employee_id):
        try:
            employee = cls.query.filter(cls.id == employee_id).first()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return employee

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise




class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    employee = relationship('Employee', backref='user', uselist=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exeption:
            session.rollback()
            raise
