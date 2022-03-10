from marshmallow import Schema, fields


class DirectorSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)