from flask import Blueprint, jsonify, request
from app.models.user import User
from app import db

api_v2 = Blueprint('api_v2', __name__)

@api_v2.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [{'username': user.username, 'email': user.email} for user in users]})

@api_v2.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'})

@api_v2.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'username': user.username, 'email': user.email})

@api_v2.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    username = request.json.get('username')
    email = request.json.get('email')
    user.username = username
    user.email = email
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

@api_v2.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})