from flask_restx import fields
from .extensions import api

todo_model = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'done': fields.Boolean(description='Completion status'),
})

todo_create_model = api.model('TodoCreate', {
    'task': fields.String(required=True, description='The task details'),
})
