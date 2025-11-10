"""
API routes package.
Contains Flask blueprints for all API endpoints.
"""

from .auth_routes import auth_bp

# Additional route blueprints will be imported as they are created
# from .candidate_routes import candidate_bp
# from .job_routes import job_bp
# from .dashboard_routes import dashboard_bp

__all__ = ['auth_bp']
