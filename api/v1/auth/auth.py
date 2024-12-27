from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from os import getenv

JWT_SECRET = getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def create_token(user_id: str) -> str:
    """Create a JWT token for a user"""
    payload = {
        'user_id': user_id,
        'exp': (datetime.now() + timedelta(hours=JWT_EXPIRATION_HOURS)),
        'lat': datetime.now().isoformat()
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token


def token_required(f):
    """Decorator to protect routes with JWT auth"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'Authorization needed'})

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # To verify token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated
