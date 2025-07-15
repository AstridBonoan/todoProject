from flask_restx import fields
from marshmallow import Schema, fields as ma_fields, validate, validates_schema, ValidationError
from app.models import TodoStatus
from .extensions import api
from datetime import datetime, timezone

# Flask-RESTX models for Swagger
todo_model = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'done': fields.Boolean(description='Completion status'),
})

todo_create_model = api.model('TodoCreate', {
    'task': fields.String(required=True, description='The task details'),
})

# Marshmallow schemas for validation/deserialization
class TodoSchema(Schema):
    id = ma_fields.Int(dump_only=True)
    task = ma_fields.Str(required=True, validate=validate.Length(min=1, max=255))
    status = ma_fields.Str(required=True, validate=validate.OneOf([status.name for status in TodoStatus]))
    category = ma_fields.Str(allow_none=True)
    due_date = ma_fields.DateTime(allow_none=True)
    tags = ma_fields.List(ma_fields.Str(), load_default=[])
    user_id = ma_fields.Int(required=True)

    @validates_schema
    def validate_due_date(self, data, **kwargs):
        # due_date cannot be in the past
        if "due_date" in data and data["due_date"] is not None:
            now = datetime.now(timezone.utc)  # aware datetime in UTC
            if data["due_date"] < now:
                raise ValidationError("due_date must not be in the past.", field_name="due_date")
