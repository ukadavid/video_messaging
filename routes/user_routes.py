from flask import Blueprint, request, jsonify
from models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(message='Welcome Back'), 200

    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='Welcome'), 201


@user_bp.route('/')
def index():
    return "Hello, World!"
