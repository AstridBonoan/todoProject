from flask import Flask, jsonify
from flask_cors import CORS
from .config import config_by_name

from .extensions import db, migrate, api, jwt, mail, cors, limiter
from .routes import register_routes

from .extensions import db, migrate, api, jwt, mail, bcrypt
from .routes import register_routes

# Import auth_bp blueprint to register it
from app.resources.auth import auth_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    limiter.init_app(app)

    # Import models so Alembic detects them
    from app import models

    # Register API routes and blueprints
    register_routes(app)
    app.register_blueprint(auth_bp)

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app
