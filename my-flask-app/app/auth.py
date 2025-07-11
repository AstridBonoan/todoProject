from flask import Blueprint, request, jsonify, current_app, url_for
from app.models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except Exception:
        return False
    return email

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_verification_token(user.email)
    verify_url = url_for('auth.verify_email', token=token, _external=True)

    # Send verification email asynchronously (simplified here)
    msg = Message("Verify your email", recipients=[user.email])
    msg.body = f"Please verify your email by clicking the link: {verify_url}"
    mail.send(msg)

    return jsonify({'msg': 'User registered. Please check your email to verify.'}), 201

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        return jsonify({'msg': 'Verification link expired or invalid'}), 400

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return jsonify({'msg': 'Account already verified.'}), 200

    user.is_verified = True
    db.session.commit()
    return jsonify({'msg': 'Email verified successfully.'}), 200
