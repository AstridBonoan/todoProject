from flask_restx import Namespace, Resource, fields
from app.models import User
from app.extensions import db

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'name': fields.String
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = api.payload
        user = User(
            username=data['username'],
            email=data['email'],
            name=data.get('name')
        )
        db.session.add(user)
        db.session.commit()
        return user, 201
