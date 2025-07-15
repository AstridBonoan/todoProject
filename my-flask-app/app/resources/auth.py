from flask import Blueprint, request, jsonify, current_app, url_for
from app.models import User
from app.extensions import db, jwt, mail
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return False
    return email

def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset')

def confirm_password_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return False
    return email

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already registered'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already taken'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    msg = Message('Please confirm your email', recipients=[user.email])
    msg.body = f'Click here to confirm your email: {confirm_url}'
    mail.send(msg)

    return jsonify({'msg': 'User registered. Please check your email to confirm.'}), 201

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return jsonify({'msg': 'The confirmation link is invalid or has expired.'}), 400

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return jsonify({'msg': 'Account already confirmed.'}), 200

    user.is_verified = True
    db.session.commit()
    return jsonify({'msg': 'You have confirmed your account. Thanks!'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Bad email or password'}), 401

    if not user.is_verified:
        return jsonify({'msg': 'Email not verified'}), 403

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        token = generate_password_reset_token(email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = f'Reset your password here: {reset_url}'
        mail.send(msg)
    # Always respond with success to avoid leaking user info
    return jsonify({'msg': 'If your email exists in our system, you will receive a reset link.'}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    email = confirm_password_reset_token(token)
    if not email:
        return jsonify({'msg': 'Invalid or expired token'}), 400
    data = request.get_json()
    password = data.get('password')
    user = User.query.filter_by(email=email).first_or_404()
    user.set_password(password)
    db.session.commit()
    return jsonify({'msg': 'Password has been reset successfully'}), 200
