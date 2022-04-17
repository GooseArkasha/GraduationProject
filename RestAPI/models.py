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
