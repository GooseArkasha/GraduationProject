from app import db, session, Base

class Employee(Base):
    __tablename__= 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    patronymic =  db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(250), nullable=False, unique=True)
    #position_id = db.Column(db.Integer, FoForeignKey(positions.id)
