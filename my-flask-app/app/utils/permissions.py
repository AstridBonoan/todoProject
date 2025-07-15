from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User

def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"msg": "Missing JWT identity"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"msg": "User not found"}), 404

            user_permissions = {
                perm.name
                for role in user.roles
                for perm in role.permissions
            }

            if permission_name not in user_permissions:
                return jsonify({"msg": f"Permission '{permission_name}' required"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"msg": "Missing JWT identity"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"msg": "User not found"}), 404

            user_roles = {role.name for role in user.roles}

            if role_name not in user_roles:
                return jsonify({"msg": f"Role '{role_name}' required"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
