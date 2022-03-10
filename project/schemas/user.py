from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str()
    surname = fields.Str()
