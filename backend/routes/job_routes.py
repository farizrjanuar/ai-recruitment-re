"""
Job Position routes for creating, retrieving, updating, and managing job positions.
"""

from flask import Blueprint, request, jsonify

from extensions import db
from services.job_service import JobService

job_bp = Blueprint('jobs', __name__)

# Initialize job service
job_service = JobService()


@job_bp.route('', methods=['POST'])
def create_job():
    """
    Create a new job position.
    
    Request Body:
        {
            "title": "Software Engineer",
            "description": "We are looking for...",
            "required_skills": ["Python", "Flask", "SQL"],
            "preferred_skills": ["Docker", "AWS"],
            "min_experience_years": 3,
            "education_level": "Bachelor's"
        }
    
    Returns:
        201: Job created successfully
        400: Validation error
    """
    try:
        data = request.get_json()
        
        # Validate request body
        if not data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Request body is required'
                }
            }), 400
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Job title is required'
                }
            }), 400
        
        if not data.get('description'):
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Job description is required'
                }
            }), 400
        
        # Create job using service
        job, error = job_service.create_job(data, creator_id=None)
        
        if error:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error
                }
            }), 400
        
        return jsonify({
            'message': 'Job position created successfully',
            'job_id': job.id,
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to create job position: {str(e)}'
            }
        }), 500


@job_bp.route('', methods=['GET'])
def list_jobs():
    """
    List all job positions.
    
    Query Parameters:
        include_inactive: Include inactive jobs (default: false)
    
    Returns:
        200: List of job positions
    """
    try:
        # Get query parameters
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        
        # Get jobs using service
        jobs, error = job_service.list_jobs(include_inactive=include_inactive)
        
        if error:
            return jsonify({
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': error
                }
            }), 500
        
        return jsonify({
            'jobs': jobs,
            'total': len(jobs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to list job positions: {str(e)}'
            }
        }), 500


@job_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    """
    Get a specific job position by ID.
    
    Path Parameters:
        job_id: Job position ID
    
    Returns:
        200: Job position details
        404: Job not found
    """
    try:
        # Get job using service
        job, error = job_service.get_job(job_id)
        
        if error:
            return jsonify({
                'error': {
                    'code': 'JOB_NOT_FOUND',
                    'message': error
                }
            }), 404
        
        return jsonify(job), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to retrieve job position: {str(e)}'
            }
        }), 500


@job_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Update an existing job position.
    
    Path Parameters:
        job_id: Job position ID
    
    Request Body:
        {
            "title": "Senior Software Engineer",
            "description": "Updated description...",
            "required_skills": ["Python", "Django"],
            "preferred_skills": ["Kubernetes"],
            "min_experience_years": 5,
            "education_level": "Master's",
            "is_active": true
        }
    
    Returns:
        200: Job updated successfully
        400: Validation error
        404: Job not found
    """
    try:
        data = request.get_json()
        
        # Validate request body
        if not data:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Request body is required'
                }
            }), 400
        
        # Update job using service
        job, error = job_service.update_job(job_id, data, creator_id=None)
        
        if error:
            if 'not found' in error.lower():
                return jsonify({
                    'error': {
                        'code': 'JOB_NOT_FOUND',
                        'message': error
                    }
                }), 404
            else:
                return jsonify({
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': error
                    }
                }), 400
        
        return jsonify({
            'message': 'Job position updated successfully',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to update job position: {str(e)}'
            }
        }), 500


@job_bp.route('/<job_id>/deactivate', methods=['POST'])
def deactivate_job(job_id):
    """
    Deactivate a job position (soft delete).
    
    Path Parameters:
        job_id: Job position ID
    
    Returns:
        200: Job deactivated successfully
        404: Job not found
    """
    try:
        # Deactivate job using service
        success, error = job_service.deactivate_job(job_id)
        
        if not success:
            return jsonify({
                'error': {
                    'code': 'JOB_NOT_FOUND',
                    'message': error
                }
            }), 404
        
        return jsonify({
            'message': 'Job position deactivated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to deactivate job position: {str(e)}'
            }
        }), 500


@job_bp.route('/<job_id>/activate', methods=['POST'])
def activate_job(job_id):
    """
    Activate a job position.
    
    Path Parameters:
        job_id: Job position ID
    
    Returns:
        200: Job activated successfully
        404: Job not found
    """
    try:
        # Activate job using service
        success, error = job_service.activate_job(job_id)
        
        if not success:
            return jsonify({
                'error': {
                    'code': 'JOB_NOT_FOUND',
                    'message': error
                }
            }), 404
        
        return jsonify({
            'message': 'Job position activated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'Failed to activate job position: {str(e)}'
            }
        }), 500
