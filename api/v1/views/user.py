from flask import jsonify, abort, request
from api.v1.views import app_views
from models.storage.db import DB
from ..auth.auth import create_token, token_required
from models.user import User


db = DB()


@app_views.route('/auth/register', methods=['POST'], strict_slashes=False)
def register():
    """registers a new user
    """
    data = request.get_json()

    required_fields = ['email', 'password', 'username']
    if not all(field in data for field in required_fields):
        return ({'message': 'Missing required Fields'}), 400
    
    # check if user exists
    existing_user = db.get_by_field('User', 'email', data['email'])
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409
    
    new_user = User(
        email=data['email'],
        username=data['username'],
        password=data['password']
    )

    saved_user = db.add('User',new_user)
    if not saved_user:
        return jsonify({'message': 'Error creating user'}), 500
    
    token = create_token(saved_user.id)

    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user':
        {
            'id': saved_user.id,
            'email': saved_user.email,
            'username': saved_user.username,
        }
    }), 201


@app_views.route('/auth/login', methods=['POST'], strict_slashes=False)
def login():
    """ login functionality"""

    data = request.get_json()

    if not all(field in data for field in ['email', 'password']):
        return jsonify({'message': 'Missing email or password'}), 400

    user = db.get_by_field('User', 'email', data['email'])
    if not user:
        return jsonify({'message': 'User does not exist'}), 401
    
    if not user.is_valid_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = create_token(user.id)
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
    })

@app_views.route('/me', methods=['GET'])
@token_required
def get_me():
    """gets current logged in user
    """
    user = db.get_by_field('User', 'id', request.user_id)
    
    if not user:
        return jsonify({'messsage': 'User not found'}), 404
    
    return jsonify({'User': user.username})