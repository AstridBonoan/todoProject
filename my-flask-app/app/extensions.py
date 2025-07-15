from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='Todo API',
    version='1.0',
    description='A simple Todo API'
)

jwt = JWTManager()
mail = Mail()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
mail = Mail()
bcrypt = Bcrypt()
