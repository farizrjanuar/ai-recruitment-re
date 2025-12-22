"""
Candidate API Routes

This module defines API endpoints for candidate management including
CV upload, candidate retrieval, and listing with filtering.
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from services.candidate_service import CandidateService


# Create Blueprint
candidate_bp = Blueprint('candidate', __name__)


@candidate_bp.route('/upload', methods=['POST'])
def upload_cv():
    """
    Upload and process a candidate CV.
    
    Endpoint: POST /api/candidates/upload
    Request: multipart/form-data with 'cv_file' field
    
    Returns:
        JSON response with candidate_id and processing status
    """
    try:
        
        # Check if file is in request
        if 'cv_file' not in request.files:
            return jsonify({
                'error': {
                    'code': 'FILE_MISSING',
                    'message': 'No file provided in request'
                }
            }), 400
        
        file = request.files['cv_file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'error': {
                    'code': 'FILE_MISSING',
                    'message': 'No file selected'
                }
            }), 400
        
        # Initialize candidate service
        upload_folder = current_app.config['UPLOAD_FOLDER']
        candidate_service = CandidateService(upload_folder)
        
        # Save uploaded file
        file_path, secure_name, error = candidate_service.save_uploaded_file(file)
        
        if error:
            return jsonify({
                'error': {
                    'code': 'FILE_INVALID_FORMAT',
                    'message': error
                }
            }), 400
        
        # Process CV (synchronous for MVP)
        candidate_profile, error = candidate_service.process_cv(file_path, file.filename)
        
        if error:
            # Clean up uploaded file
            candidate_service.delete_file(file_path)
            
            # Determine error code based on error message
            if 'size' in error.lower():
                error_code = 'FILE_TOO_LARGE'
            elif 'format' in error.lower():
                error_code = 'FILE_INVALID_FORMAT'
            elif 'extract' in error.lower() or 'read' in error.lower():
                error_code = 'FILE_UNREADABLE'
            elif 'content' in error.lower() or 'text' in error.lower():
                error_code = 'FILE_UNREADABLE'
            else:
                error_code = 'PROCESSING_ERROR'
            
            return jsonify({
                'error': {
                    'code': error_code,
                    'message': error
                }
            }), 400
        
        # Create candidate record in database
        candidate, error = candidate_service.create_candidate(candidate_profile)
        
        if error:
            # Clean up uploaded file
            candidate_service.delete_file(file_path)
            
            if 'already exists' in error.lower():
                return jsonify({
                    'error': {
                        'code': 'CANDIDATE_DUPLICATE',
                        'message': error
                    }
                }), 409
            
            return jsonify({
                'error': {
                    'code': 'DATABASE_ERROR',
                    'message': error
                }
            }), 500
        
        # Clean up uploaded file after successful processing
        # (we store the text in database, don't need the file anymore)
        candidate_service.delete_file(file_path)
        
        # Automatically calculate matches with all active job positions
        try:
            from services.matching_service import MatchingService
            matching_service = MatchingService()
            matches = matching_service.calculate_matches(candidate.id)
            match_count = len(matches)
        except Exception as e:
            # Matching failure shouldn't block the upload response
            print(f"Warning: Failed to calculate matches for candidate {candidate.id}: {str(e)}")
            match_count = 0
        
        # Prepare response
        response = {
            'candidate_id': candidate.id,
            'status': candidate.status,
            'message': 'CV uploaded and processed successfully',
            'matches_calculated': match_count
        }
        
        # Add warnings if extraction had issues
        if candidate_profile.get('extraction_errors'):
            response['warnings'] = candidate_profile['extraction_errors']
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'An unexpected error occurred: {str(e)}'
            }
        }), 500


@candidate_bp.route('', methods=['GET'])
def list_candidates():
    """
    List all candidates with pagination and filtering.
    
    Endpoint: GET /api/candidates
    Query Parameters:
        - page: Page number (default: 1)
        - limit: Items per page (default: 20, max: 100)
        - status: Filter by status ('processing', 'completed', 'failed')
        - skills: Comma-separated list of skills to filter by
    
    Returns:
        JSON response with candidates list and pagination info
    """
    try:
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status = request.args.get('status', None, type=str)
        skills_param = request.args.get('skills', None, type=str)
        
        # Validate pagination parameters
        if page < 1:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Page number must be greater than 0'
                }
            }), 400
        
        if limit < 1 or limit > 100:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Limit must be between 1 and 100'
                }
            }), 400
        
        # Validate status parameter
        if status and status not in ['processing', 'completed', 'failed']:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Invalid status. Must be one of: processing, completed, failed'
                }
            }), 400
        
        # Parse skills parameter
        skills = None
        if skills_param:
            skills = [s.strip() for s in skills_param.split(',') if s.strip()]
        
        # Initialize candidate service
        upload_folder = current_app.config['UPLOAD_FOLDER']
        candidate_service = CandidateService(upload_folder)
        
        # Get candidates
        result, error = candidate_service.list_candidates(
            page=page,
            limit=limit,
            status=status,
            skills=skills
        )
        
        if error:
            return jsonify({
                'error': {
                    'code': 'DATABASE_ERROR',
                    'message': error
                }
            }), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'An unexpected error occurred: {str(e)}'
            }
        }), 500


@candidate_bp.route('/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """
    Get detailed information about a specific candidate.
    
    Endpoint: GET /api/candidates/<candidate_id>
    Query Parameters:
        - include_raw_text: Include raw CV text (default: false)
    
    Returns:
        JSON response with complete candidate profile
    """
    try:
        
        # Get query parameters
        include_raw_text = request.args.get('include_raw_text', 'false').lower() == 'true'
        
        # Initialize candidate service
        upload_folder = current_app.config['UPLOAD_FOLDER']
        candidate_service = CandidateService(upload_folder)
        
        # Get candidate
        candidate_data, error = candidate_service.get_candidate(
            candidate_id,
            include_raw_text=include_raw_text
        )
        
        if error:
            if 'not found' in error.lower():
                return jsonify({
                    'error': {
                        'code': 'CANDIDATE_NOT_FOUND',
                        'message': error
                    }
                }), 404
            
            return jsonify({
                'error': {
                    'code': 'DATABASE_ERROR',
                    'message': error
                }
            }), 500
        
        return jsonify(candidate_data), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'An unexpected error occurred: {str(e)}'
            }
        }), 500


@candidate_bp.route('/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """
    Delete a candidate permanently.
    
    Endpoint: DELETE /api/candidates/<candidate_id>
    
    Returns:
        200: Candidate deleted successfully
        404: Candidate not found
        500: Internal server error
    """
    try:
        # Initialize candidate service
        upload_folder = current_app.config['UPLOAD_FOLDER']
        candidate_service = CandidateService(upload_folder)
        
        # Delete candidate
        success, error = candidate_service.delete_candidate(candidate_id)
        
        if not success:
            if 'not found' in error.lower():
                return jsonify({
                    'error': {
                        'code': 'CANDIDATE_NOT_FOUND',
                        'message': error
                    }
                }), 404
            else:
                return jsonify({
                    'error': {
                        'code': 'DELETE_ERROR',
                        'message': error
                    }
                }), 500
        
        return jsonify({
            'message': 'Candidate deleted successfully',
            'candidate_id': candidate_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'An unexpected error occurred: {str(e)}'
            }
        }), 500
