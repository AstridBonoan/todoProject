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


# Initialize Flask extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    limiter.init_app(app)

    # Register API routes
    register_routes(app)

    bcrypt.init_app(app)

    # Enable CORS for the React frontend running on localhost:5173
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Register API routes (Flask-RESTX namespaces)
    register_routes(app)

    # Register the auth blueprint separately (since it’s not a Flask-RESTX namespace)
    app.register_blueprint(auth_bp)

    # Simple health check endpoint for uptime monitoring
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app
