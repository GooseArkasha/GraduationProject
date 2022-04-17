from marshmallow import Schema, validate, fields


class EmployeeSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True, validate=[validate.Length(max=250)])
    last_name = fields.String(required=True, validate=[validate.Length(max=250)])
    patronymic =  fields.String(validate=[validate.Length(max=250)])
    email = fields.String(required=True, validate=[validate.Length(max=250)])
    phone_number = fields.String(required=True, validate=[validate.Length(max=250)])
    user_id = fields.Integer()
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String(required=True, validate=[
        validate.Length(max=250)])
    password = fields.String(required=True, validate=[
        validate.Length(max=250)], load_only=True)
    employee = fields.Nested(EmployeeSchema, dump_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
