from flask_restx import Resource, Namespace, fields, reqparse
from flask import request
from app.models import db, Todo, TodoStatus, Tag, User
from sqlalchemy.exc import NoResultFound
from datetime import datetime

api = Namespace('todos', description='Todo operations')

todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True),
    'task': fields.String(required=True),
    'status': fields.String(enum=[e.value for e in TodoStatus]),
    'category': fields.String,
    'due_date': fields.DateTime,
    'tags': fields.List(fields.String),
    'user_id': fields.Integer(required=True),
})

parser = reqparse.RequestParser()
parser.add_argument('task', required=True, help='Task cannot be blank')
parser.add_argument('status', choices=[e.value for e in TodoStatus])
parser.add_argument('user_id', type=int, required=True, help='User ID is required')
parser.add_argument('category')
parser.add_argument('due_date')
parser.add_argument('tags', type=list, location='json')


def parse_iso_datetime(date_str):
    if not date_str:
        return None
    try:
        # Replace Z with +00:00 for UTC timezone awareness
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        api.abort(400, "Invalid date format for due_date. Use ISO8601 format.")


@api.route('/')
class TodoListResource(Resource):
    @api.marshal_list_with(todo_model)
    def get(self):
        todos = Todo.query.filter_by(is_deleted=False).all()
        return todos

    @api.expect(todo_model)
    @api.marshal_with(todo_model, code=201)
    def post(self):
        data = api.payload

        user_id = data.get('user_id')
        if not user_id:
            api.abort(400, "user_id is required")

        user = User.query.get(user_id)
        if not user:
            api.abort(400, f"User with id {user_id} does not exist")

        due_date = parse_iso_datetime(data.get('due_date'))

        todo = Todo(
            task=data['task'],
            status=TodoStatus(data.get('status', 'pending')),
            category=data.get('category'),
            due_date=due_date,
            user_id=user_id
        )

        tag_names = data.get('tags') or []
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

        return todo, 201


@api.route('/<int:id>')
@api.param('id', 'The todo identifier')
class TodoItemResource(Resource):
    @api.marshal_with(todo_model)
    def get(self, id):
        todo = Todo.query.get_or_404(id)
        return todo

    @api.expect(todo_model)
    @api.marshal_with(todo_model)
    def put(self, id):
        todo = Todo.query.get_or_404(id)
        data = api.payload

        todo.task = data.get('task', todo.task)
        todo.status = TodoStatus(data.get('status', todo.status.value))
        todo.category = data.get('category', todo.category)

        due_date = parse_iso_datetime(data.get('due_date'))
        if due_date is not None:
            todo.due_date = due_date

        tag_names = data.get('tags')
        if tag_names is not None:
            tags = []
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
            todo.tags = tags

        db.session.commit()
        return todo

    def delete(self, id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204


@api.route('/<int:id>/toggle')
@api.param('id', 'The todo identifier')
class TodoToggleResource(Resource):
    @api.marshal_with(todo_model)
    def patch(self, id):
        todo = Todo.query.get_or_404(id)
        if todo.status == TodoStatus.COMPLETED:
            todo.status = TodoStatus.PENDING
        else:
            todo.status = TodoStatus.COMPLETED
        db.session.commit()
        return todo
