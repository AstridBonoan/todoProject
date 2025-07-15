from flask_restx import Resource, Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.models import db, Todo, TodoStatus, Tag, User
from app.schemas import TodoSchema
from app.utils.permissions import permission_required  # custom decorator
from marshmallow import ValidationError
from datetime import datetime

api = Namespace('todos', description='Todo operations')

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# RESTX model for Swagger documentation only
todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True),
    'task': fields.String(required=True),
    'status': fields.String,
    'category': fields.String,
    'due_date': fields.DateTime,
    'tags': fields.List(fields.String),
    'user_id': fields.Integer(required=True),
})

def parse_iso_datetime(date_val):
    if not date_val:
        return None
    if isinstance(date_val, str):
        try:
            # Replace Zulu time suffix with +00:00 for UTC
            return datetime.fromisoformat(date_val.replace('Z', '+00:00'))
        except ValueError:
            api.abort(400, "Invalid date format for due_date. Use ISO8601 format.")
    elif isinstance(date_val, datetime):
        return date_val
    else:
        api.abort(400, "Invalid type for due_date")

@api.route('/')
class TodoListResource(Resource):
    @jwt_required()
    @permission_required('view_todo')
    def get(self):
        todos = Todo.query.filter_by(is_deleted=False).all()
        return todos_schema.dump(todos), 200

    @jwt_required()
    @permission_required('create_todo')
    @api.expect(todo_model)
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            todo_data = todo_schema.load(json_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        user_id = todo_data.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return {"message": f"User with id {user_id} does not exist"}, 400

        due_date = parse_iso_datetime(todo_data.get('due_date'))

        # Normalize status string to lowercase before converting to enum
        status_str = todo_data.get('status', 'pending')
        status_str = status_str.lower() if status_str else 'pending'

        todo = Todo(
            task=todo_data['task'],
            status=TodoStatus(status_str),
            category=todo_data.get('category'),
            due_date=due_date,
            user_id=user_id
        )

        tag_names = todo_data.get('tags') or []
        tags = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)
        todo.tags = tags

        db.session.add(todo)
        db.session.commit()

        return todo_schema.dump(todo), 201

@api.route('/<int:id>')
@api.param('id', 'The todo identifier')
class TodoItemResource(Resource):
    @jwt_required()
    @permission_required('view_todo')
    def get(self, id):
        todo = Todo.query.get_or_404(id)
        return todo_schema.dump(todo), 200

    @jwt_required()
    @permission_required('edit_todo')
    @api.expect(todo_model)
    def put(self, id):
        todo = Todo.query.get_or_404(id)
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        try:
            todo_data = todo_schema.load(json_data, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

        todo.task = todo_data.get('task', todo.task)

        if 'status' in todo_data:
            status_str = todo_data['status']
            status_str = status_str.lower() if status_str else todo.status.value
            todo.status = TodoStatus(status_str)

        todo.category = todo_data.get('category', todo.category)

        if 'due_date' in todo_data:
            todo.due_date = parse_iso_datetime(todo_data['due_date'])

        if 'tags' in todo_data:
            tag_names = todo_data['tags']
            tags = []
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
            todo.tags = tags

        db.session.commit()
        return todo_schema.dump(todo), 200

    @jwt_required()
    @permission_required('delete_todo')
    def delete(self, id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

@api.route('/<int:id>/toggle')
@api.param('id', 'The todo identifier')
class TodoToggleResource(Resource):
    @jwt_required()
    @permission_required('edit_todo')
    def patch(self, id):
        todo = Todo.query.get_or_404(id)
        todo.status = (
            TodoStatus.PENDING if todo.status == TodoStatus.COMPLETED else TodoStatus.COMPLETED
        )
        db.session.commit()
        return todo_schema.dump(todo), 200
