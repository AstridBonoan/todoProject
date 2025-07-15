from app.resources.todo import api as todo_ns
from app.resources.user import api as user_ns
<<<<<<< HEAD
from app.extensions import api

def register_routes(app):
    api.add_namespace(todo_ns, path='/api/todos')
    api.add_namespace(user_ns, path='/api/users')
=======
from app.resources.auth import auth_bp
from app.extensions import api

def register_routes(app):
    # Register Flask-RESTX namespaces
    api.add_namespace(todo_ns, path='/api/todos')
    api.add_namespace(user_ns, path='/api/users')

>>>>>>> 77732ee (Initial commit with updated Flask todo app)
