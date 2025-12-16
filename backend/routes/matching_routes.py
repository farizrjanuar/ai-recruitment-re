"""
Matching API Routes

This module provides REST API endpoints for candidate-job matching operations.
"""

from flask import Blueprint, jsonify, request
from services.matching_service import MatchingService


# Create blueprint
matching_bp = Blueprint('matching', __name__)

# Initialize service
matching_service = MatchingService()


@matching_bp.route('/calculate/<candidate_id>', methods=['POST'])
def calculate_matches(candidate_id):
    """
    Calculate match scores for a candidate against all active job positions.
    
    POST /api/matching/calculate/:candidate_id
    
    Returns:
        200: Match results calculated successfully
        400: Invalid request or candidate data incomplete
        404: Candidate not found
        500: Internal server error
    """
    try:
        # Calculate matches for the candidate
        matches = matching_service.calculate_matches(candidate_id)
        
        return jsonify({
            'candidate_id': candidate_id,
            'matches': matches,
            'total_matches': len(matches)
        }), 200
        
    except ValueError as e:
        # Handle validation errors (candidate not found, incomplete profile, etc.)
        error_message = str(e)
        
        if 'not found' in error_message.lower():
            return jsonify({
                'error': {
                    'code': 'CANDIDATE_NOT_FOUND',
                    'message': error_message
                }
            }), 404
        else:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_message
                }
            }), 400
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            'error': {
                'code': 'PROCESSING_ERROR',
                'message': f'Failed to calculate matches: {str(e)}'
            }
        }), 500


@matching_bp.route('/job/<job_id>', methods=['GET'])
def get_job_candidates(job_id):
    """
    Get ranked list of candidates for a specific job position.
    
    GET /api/matching/job/:job_id
    
    Query Parameters:
        min_score (optional): Minimum match score threshold (0-100)
        status (optional): Filter by qualification status 
                          ('Qualified', 'Potentially Qualified', 'Not Qualified', 'all')
        limit (optional): Maximum number of results to return
    
    Returns:
        200: Candidate matches retrieved successfully
        400: Invalid query parameters
        404: Job position not found
        500: Internal server error
    """
    try:
        # Parse query parameters
        min_score = request.args.get('min_score', type=float)
        status_filter = request.args.get('status', 'all')
        limit = request.args.get('limit', type=int)
        
        # Validate min_score if provided
        if min_score is not None and (min_score < 0 or min_score > 100):
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'min_score must be between 0 and 100'
                }
            }), 400
        
        # Validate status filter
        valid_statuses = ['Qualified', 'Potentially Qualified', 'Not Qualified', 'all']
        if status_filter not in valid_statuses:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'status must be one of: {", ".join(valid_statuses)}'
                }
            }), 400
        
        # Validate limit if provided
        if limit is not None and limit < 1:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'limit must be a positive integer'
                }
            }), 400
        
        # Get candidates for the job
        candidates = matching_service.get_candidates_for_job(
            job_id=job_id,
            min_score=min_score,
            status_filter=status_filter,
            limit=limit
        )
        
        # Get job details
        from models.job_position import JobPosition
        job = JobPosition.query.get(job_id)
        
        return jsonify({
            'job_id': job_id,
            'job_title': job.title if job else None,
            'candidates': candidates,
            'total_candidates': len(candidates),
            'filters': {
                'min_score': min_score,
                'status': status_filter,
                'limit': limit
            }
        }), 200
        
    except ValueError as e:
        # Handle validation errors (job not found, etc.)
        error_message = str(e)
        
        if 'not found' in error_message.lower():
            return jsonify({
                'error': {
                    'code': 'JOB_NOT_FOUND',
                    'message': error_message
                }
            }), 404
        else:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_message
                }
            }), 400
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            'error': {
                'code': 'PROCESSING_ERROR',
                'message': f'Failed to retrieve candidates: {str(e)}'
            }
        }), 500


@matching_bp.route('/candidate/<candidate_id>', methods=['GET'])
def get_candidate_matches(candidate_id):
    """
    Get all match results for a specific candidate.
    
    GET /api/matching/candidate/:candidate_id
    
    Query Parameters:
        min_score (optional): Minimum match score threshold (0-100)
    
    Returns:
        200: Match results retrieved successfully
        400: Invalid query parameters
        404: Candidate not found
        500: Internal server error
    """
    try:
        # Parse query parameters
        min_score = request.args.get('min_score', type=float)
        
        # Validate min_score if provided
        if min_score is not None and (min_score < 0 or min_score > 100):
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'min_score must be between 0 and 100'
                }
            }), 400
        
        # Get matches for the candidate
        matches = matching_service.get_candidate_matches(
            candidate_id=candidate_id,
            min_score=min_score
        )
        
        # Get candidate details
        from models.candidate import Candidate
        candidate = Candidate.query.get(candidate_id)
        
        return jsonify({
            'candidate_id': candidate_id,
            'candidate_name': candidate.name if candidate else None,
            'matches': matches,
            'total_matches': len(matches),
            'filters': {
                'min_score': min_score
            }
        }), 200
        
    except ValueError as e:
        # Handle validation errors (candidate not found, etc.)
        error_message = str(e)
        
        if 'not found' in error_message.lower():
            return jsonify({
                'error': {
                    'code': 'CANDIDATE_NOT_FOUND',
                    'message': error_message
                }
            }), 404
        else:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_message
                }
            }), 400
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            'error': {
                'code': 'PROCESSING_ERROR',
                'message': f'Failed to retrieve matches: {str(e)}'
            }
        }), 500


@matching_bp.route('/single/<candidate_id>/<job_id>', methods=['POST'])
def calculate_single_match(candidate_id, job_id):
    """
    Calculate match score for a specific candidate-job pair.
    
    POST /api/matching/single/:candidate_id/:job_id
    
    Returns:
        200: Match calculated successfully
        400: Invalid request or incomplete data
        404: Candidate or job not found
        500: Internal server error
    """
    try:
        # Calculate single match
        match_result = matching_service.calculate_single_match(candidate_id, job_id)
        
        return jsonify({
            'match': match_result
        }), 200
        
    except ValueError as e:
        # Handle validation errors
        error_message = str(e)
        
        if 'not found' in error_message.lower():
            return jsonify({
                'error': {
                    'code': 'NOT_FOUND',
                    'message': error_message
                }
            }), 404
        else:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_message
                }
            }), 400
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            'error': {
                'code': 'PROCESSING_ERROR',
                'message': f'Failed to calculate match: {str(e)}'
            }
        }), 500
