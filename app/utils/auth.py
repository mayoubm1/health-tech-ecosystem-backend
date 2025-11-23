"""
Authentication Utilities
"""

import jwt
import os
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')

def hash_password(password):
    """Hash a password"""
    return generate_password_hash(password)

def verify_password(password, hash_):
    """Verify a password against its hash"""
    return check_password_hash(hash_, password)

def create_jwt_token(user_id, email, role):
    """Create a JWT token"""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Authorization token is required'}), 401
        
        user_data = verify_jwt_token(token)
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(user_data, *args, **kwargs)
    return decorated
