"""
Authentication decorators for role-based access control.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User


def admin_required():
    """
    Decorator to require Admin role for accessing an endpoint.
    Must be used after @jwt_required() decorator.
    
    Usage:
        @app.route('/admin-only')
        @jwt_required()
        @admin_required()
        def admin_endpoint():
            return jsonify({'message': 'Admin access granted'})
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT is present
            verify_jwt_in_request()
            
            # Get current user
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({
                    'error': {
                        'code': 'AUTH_TOKEN_INVALID',
                        'message': 'User not found'
                    }
                }), 401
            
            # Check if user has Admin role
            if user.role != 'Admin':
                return jsonify({
                    'error': {
                        'code': 'AUTH_INSUFFICIENT_PERMISSIONS',
                        'message': 'Admin access required'
                    }
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def hr_required():
    """
    Decorator to require HR or Admin role for accessing an endpoint.
    Must be used after @jwt_required() decorator.
    
    Usage:
        @app.route('/hr-endpoint')
        @jwt_required()
        @hr_required()
        def hr_endpoint():
            return jsonify({'message': 'HR access granted'})
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT is present
            verify_jwt_in_request()
            
            # Get current user
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({
                    'error': {
                        'code': 'AUTH_TOKEN_INVALID',
                        'message': 'User not found'
                    }
                }), 401
            
            # Check if user has HR or Admin role
            if user.role not in ['HR', 'Admin']:
                return jsonify({
                    'error': {
                        'code': 'AUTH_INSUFFICIENT_PERMISSIONS',
                        'message': 'HR or Admin access required'
                    }
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user():
    """
    Helper function to get the current authenticated user.
    Must be called within a JWT-protected route.
    
    Returns:
        User: Current user object or None if not found
    """
    try:
        current_user_id = get_jwt_identity()
        return User.query.get(current_user_id)
    except Exception:
        return None
