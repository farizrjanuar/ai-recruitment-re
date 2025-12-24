"""
AI Recruitment System - Flask Application Entry Point
Main application factory and initialization.
"""

import os
from flask import Flask, jsonify
from config import config
from extensions import db, cors


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
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes.candidate_routes import candidate_bp
    from routes.job_routes import job_bp
    from routes.matching_routes import matching_bp
    from routes.dashboard_routes import dashboard_bp
    
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
        from models import Candidate, JobPosition, MatchResult
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
