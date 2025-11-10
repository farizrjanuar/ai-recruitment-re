"""
Dashboard routes for HR analytics and statistics.
Provides endpoints for retrieving recruitment metrics and data visualizations.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from models.user import User
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)


def hr_or_admin_required():
    """
    Decorator to require HR or Admin role for accessing endpoints.
    Must be used after @jwt_required().
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({
                    'error': {
                        'code': 'AUTH_TOKEN_INVALID',
                        'message': 'User not found'
                    }
                }), 401
            
            if user.role not in ['HR', 'Admin']:
                return jsonify({
                    'error': {
                        'code': 'AUTH_INSUFFICIENT_PERMISSIONS',
                        'message': 'HR or Admin role required'
                    }
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
@hr_or_admin_required()
def get_statistics():
    """
    Get overall recruitment statistics for the dashboard.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Statistics data
            {
                "total_candidates": 150,
                "total_jobs": 12,
                "avg_match_score": 67.5,
                "qualified_candidates": 45,
                "recent_uploads": 8
            }
        401: Unauthorized
        403: Insufficient permissions
        500: Internal server error
    
    Requirements: 7.1, 7.5
    """
    try:
        # Get statistics from service
        stats = DashboardService.get_statistics()
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to retrieve statistics: {str(e)}'
            }
        }), 500


@dashboard_bp.route('/analytics', methods=['GET'])
@jwt_required()
@hr_or_admin_required()
def get_analytics():
    """
    Get detailed analytics data for visualizations.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Analytics data
            {
                "skill_distribution": {
                    "Python": 45,
                    "JavaScript": 38,
                    "SQL": 32,
                    ...
                },
                "experience_distribution": {
                    "0-2 years": 25,
                    "3-5 years": 40,
                    "6-10 years": 35,
                    "11-15 years": 20,
                    "16+ years": 10
                },
                "match_score_distribution": {
                    "0-20": 5,
                    "21-40": 15,
                    "41-60": 30,
                    "61-80": 40,
                    "81-100": 20
                }
            }
        401: Unauthorized
        403: Insufficient permissions
        500: Internal server error
    
    Requirements: 7.1, 7.5
    """
    try:
        # Get analytics from service
        analytics = DashboardService.get_analytics()
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to retrieve analytics: {str(e)}'
            }
        }), 500
