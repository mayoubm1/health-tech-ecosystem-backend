"""
Authentication Routes
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Profile
from app.utils.auth import hash_password, verify_password, create_jwt_token, verify_jwt_token
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            password_hash=hash_password(data['password']),
            role=data.get('role', 'patient')
        )
        
        db.session.add(user)
        db.session.flush()
        
        # Create user profile
        profile = Profile(id=user.id)
        db.session.add(profile)
        db.session.commit()
        
        # Generate JWT token
        token = create_jwt_token(user.id, user.email, user.role)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not verify_password(data['password'], user.password_hash):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Generate JWT token
        token = create_jwt_token(user.id, user.email, user.role)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user information"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Authorization token is required'}), 401
        
        user_data = verify_jwt_token(token)
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(user_data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'profile': user.profile.to_dict() if user.profile else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh JWT token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Authorization token is required'}), 401
        
        user_data = verify_jwt_token(token)
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(user_data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate new token
        new_token = create_jwt_token(user.id, user.email, user.role)
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logout successful'}), 200
