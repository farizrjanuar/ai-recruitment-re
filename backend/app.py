"""
AI Recruitment System - Flask Application Entry Point
Main application factory and initialization.
"""

import os
from flask import Flask, jsonify
from config import config
from extensions import db, jwt, cors


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name: Configuration environment name ('development', 'production', 'testing')
    
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.candidate_routes import candidate_bp
    from routes.job_routes import job_bp
    from routes.matching_routes import matching_bp
    from routes.dashboard_routes import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(candidate_bp, url_prefix='/api/candidates')
    app.register_blueprint(job_bp, url_prefix='/api/jobs')
    app.register_blueprint(matching_bp, url_prefix='/api/matching')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({
            'status': 'healthy',
            'message': 'AI Recruitment System API is running'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'name': 'AI Recruitment System API',
            'version': '1.0.0',
            'status': 'active'
        }), 200
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired JWT tokens."""
        return jsonify({
            'error': {
                'code': 'AUTH_TOKEN_EXPIRED',
                'message': 'The token has expired'
            }
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid JWT tokens."""
        return jsonify({
            'error': {
                'code': 'AUTH_TOKEN_INVALID',
                'message': 'Invalid token'
            }
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing JWT tokens."""
        return jsonify({
            'error': {
                'code': 'AUTH_TOKEN_MISSING',
                'message': 'Authorization token is required'
            }
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked JWT tokens."""
        return jsonify({
            'error': {
                'code': 'AUTH_TOKEN_REVOKED',
                'message': 'The token has been revoked'
            }
        }), 401
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found'
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred'
            }
        }), 500
    
    # Import models to ensure they are registered with SQLAlchemy
    with app.app_context():
        from models import User, Candidate, JobPosition, MatchResult
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
