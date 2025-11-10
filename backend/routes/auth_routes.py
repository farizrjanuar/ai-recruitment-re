"""
Authentication routes for user registration, login, and token management.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from extensions import db
from models.user import User
import re

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    return True, ""


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123",
            "role": "HR" (optional, defaults to "HR")
        }
    
    Returns:
        201: User created successfully
        400: Validation error or user already exists
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Request body is required'
                }
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        role = data.get('role', 'HR').strip()
        
        # Validate email
        if not email:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email is required'
                }
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid email format'
                }
            }), 400
        
        # Validate password
        if not password:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Password is required'
                }
            }), 400
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_msg
                }
            }), 400
        
        # Validate role
        if role not in ['Admin', 'HR']:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Role must be either "Admin" or "HR"'
                }
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'User with this email already exists'
                }
            }), 400
        
        # Create new user
        new_user = User(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to register user: {str(e)}'
            }
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and generate JWT tokens.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "SecurePass123"
        }
    
    Returns:
        200: Login successful with access and refresh tokens
        401: Invalid credentials
        400: Validation error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Request body is required'
                }
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Email and password are required'
                }
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Verify credentials
        if not user or not user.check_password(password):
            return jsonify({
                'error': {
                    'code': 'AUTH_INVALID_CREDENTIALS',
                    'message': 'Invalid email or password'
                }
            }), 401
        
        # Generate JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Login failed: {str(e)}'
            }
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Returns:
        200: New access token generated
        401: Invalid or expired refresh token
    """
    try:
        # Get user identity from refresh token
        current_user_id = get_jwt_identity()
        
        # Verify user still exists
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'error': {
                    'code': 'AUTH_TOKEN_INVALID',
                    'message': 'User not found'
                }
            }), 401
        
        # Generate new access token
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Token refresh failed: {str(e)}'
            }
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: User information
        401: Invalid or expired token
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'error': {
                    'code': 'AUTH_TOKEN_INVALID',
                    'message': 'User not found'
                }
            }), 401
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to get user: {str(e)}'
            }
        }), 500
