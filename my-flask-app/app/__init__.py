from flask import Flask, jsonify
from flask_cors import CORS
from .config import config_by_name
from .extensions import db, migrate, api, jwt, mail, cors, limiter
from .routes import register_routes

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    limiter.init_app(app)

    # Register API routes
    register_routes(app)

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app
