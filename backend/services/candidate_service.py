"""
Candidate Service

This service provides business logic for candidate management including
CV processing, candidate creation, retrieval, and listing with filtering.
"""

import os
from typing import Dict, List, Optional, Tuple
from werkzeug.datastructures import FileStorage

from extensions import db
from models.candidate import Candidate
from ml.text_extractor import TextExtractor
from services.cv_parser_service import CVParserService
from ml.skill_analyzer import SkillAnalyzer
from utils.file_validators import FileValidator


class CandidateService:
    """
    Service for managing candidate operations and CV processing workflow.
    
    Orchestrates:
    - File validation and storage
    - Text extraction from CVs
    - CV parsing and information extraction
    - Skill analysis
    - Candidate profile creation and management
    """
    
    def __init__(self, upload_folder: str):
        """
        Initialize the Candidate Service.
        
        Args:
            upload_folder: Directory path for storing uploaded CV files
        """
        self.upload_folder = upload_folder
        self.file_validator = FileValidator()
        self.text_extractor = TextExtractor()
        self.cv_parser = CVParserService()
        self.skill_analyzer = SkillAnalyzer()
        
        # Ensure upload folder exists
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def process_cv(self, file_path: str, filename: str) -> Tuple[Dict, Optional[str]]:
        """
        Process a CV file through the complete extraction and analysis pipeline.
        
        Workflow:
        1. Validate file
        2. Extract text from file
        3. Parse CV to extract structured information
        4. Analyze skills
        5. Return structured candidate profile
        
        Args:
            file_path: Path to the uploaded CV file
            filename: Original filename
            
        Returns:
            Tuple of (candidate_profile_dict, error_message)
            - candidate_profile_dict: Structured candidate data
            - error_message: None if successful, error description if failed
        """
        try:
            # Step 1: Validate file
            is_valid, error = self.file_validator.validate_file(file_path, filename)
            if not is_valid:
                return None, error
            
            # Step 2: Extract text from file
            file_extension = self.file_validator.get_file_extension(filename)
            
            try:
                raw_text = self.text_extractor.extract_text(file_path, file_extension)
            except Exception as e:
                return None, f"Failed to extract text from file: {str(e)}"
            
            # Step 3: Validate extracted text content
            is_valid, error = self.file_validator.validate_file_content(raw_text)
            if not is_valid:
                return None, error
            
            # Step 4: Parse CV to extract structured information
            try:
                parsed_profile = self.cv_parser.parse_cv(raw_text)
            except Exception as e:
                return None, f"Failed to parse CV: {str(e)}"
            
            # Step 5: Analyze skills from the CV text
            try:
                skills = self.skill_analyzer.analyze_skills(raw_text)
            except Exception as e:
                # Skills analysis failure shouldn't block the entire process
                skills = []
                print(f"Warning: Skill analysis failed: {str(e)}")
            
            # Step 6: Combine all extracted information
            candidate_profile = {
                'name': parsed_profile.get('name'),
                'email': parsed_profile.get('email'),
                'phone': parsed_profile.get('phone'),
                'raw_cv_text': raw_text,
                'education': parsed_profile.get('education', []),
                'experience': parsed_profile.get('experience', []),
                'skills': skills,
                'certifications': [],  # Can be enhanced later
                'total_experience_years': parsed_profile.get('total_experience_years', 0),
                'extraction_status': parsed_profile.get('extraction_status', 'success'),
                'extraction_errors': parsed_profile.get('extraction_errors', [])
            }
            
            return candidate_profile, None
            
        except Exception as e:
            return None, f"Unexpected error during CV processing: {str(e)}"
    
    def create_candidate(self, candidate_data: Dict) -> Tuple[Optional[Candidate], Optional[str]]:
        """
        Create a new candidate record in the database.
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            Tuple of (candidate_instance, error_message)
            - candidate_instance: Created Candidate object or None if failed
            - error_message: None if successful, error description if failed
        """
        try:
            # Check if candidate with this email already exists
            email = candidate_data.get('email')
            if email:
                existing_candidate = Candidate.query.filter_by(email=email).first()
                if existing_candidate:
                    return None, f"Candidate with email {email} already exists"
            
            # Determine status based on extraction results
            extraction_status = candidate_data.get('extraction_status', 'success')
            
            if extraction_status == 'failed':
                status = 'failed'
            elif extraction_status == 'partial':
                status = 'completed'  # Still usable, just with some missing data
            else:
                status = 'completed'
            
            # Create new candidate instance
            candidate = Candidate(
                name=candidate_data.get('name'),
                email=candidate_data.get('email'),
                phone=candidate_data.get('phone'),
                raw_cv_text=candidate_data.get('raw_cv_text'),
                total_experience_years=candidate_data.get('total_experience_years', 0),
                status=status
            )
            
            # Set JSON fields using setter methods
            candidate.set_education(candidate_data.get('education', []))
            candidate.set_experience(candidate_data.get('experience', []))
            candidate.set_skills(candidate_data.get('skills', []))
            candidate.set_certifications(candidate_data.get('certifications', []))
            
            # Save to database
            db.session.add(candidate)
            db.session.commit()
            
            return candidate, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create candidate: {str(e)}"
    
    def get_candidate(self, candidate_id: str, include_raw_text: bool = False) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Retrieve a candidate by ID.
        
        Args:
            candidate_id: Candidate's unique identifier
            include_raw_text: Whether to include raw CV text in response
            
        Returns:
            Tuple of (candidate_dict, error_message)
            - candidate_dict: Candidate data or None if not found
            - error_message: None if successful, error description if failed
        """
        try:
            candidate = Candidate.query.get(candidate_id)
            
            if not candidate:
                return None, f"Candidate with ID {candidate_id} not found"
            
            return candidate.to_dict(include_raw_text=include_raw_text), None
            
        except Exception as e:
            return None, f"Failed to retrieve candidate: {str(e)}"
    
    def list_candidates(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        skills: Optional[List[str]] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        List candidates with pagination and filtering.
        
        Args:
            page: Page number (1-indexed)
            limit: Number of candidates per page
            status: Filter by status ('processing', 'completed', 'failed')
            skills: Filter by skills (list of skill names)
            
        Returns:
            Tuple of (result_dict, error_message)
            - result_dict: Contains 'candidates', 'total', 'page', 'pages'
            - error_message: None if successful, error description if failed
        """
        try:
            # Build query
            query = Candidate.query
            
            # Apply status filter
            if status:
                query = query.filter_by(status=status)
            
            # Apply skills filter (if provided)
            if skills and len(skills) > 0:
                # Filter candidates who have at least one of the specified skills
                # This requires checking the JSON field
                for skill in skills:
                    # Use JSON contains for PostgreSQL or simple string search for SQLite
                    query = query.filter(
                        Candidate.skills.contains(skill) |
                        db.cast(Candidate.skills, db.String).like(f'%{skill}%')
                    )
            
            # Get total count before pagination
            total = query.count()
            
            # Apply pagination
            pagination = query.order_by(Candidate.created_at.desc()).paginate(
                page=page,
                per_page=limit,
                error_out=False
            )
            
            # Convert candidates to dictionaries
            candidates = [candidate.to_dict(include_raw_text=False) for candidate in pagination.items]
            
            result = {
                'candidates': candidates,
                'total': total,
                'page': page,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
            
            return result, None
            
        except Exception as e:
            return None, f"Failed to list candidates: {str(e)}"
    
    def update_candidate_status(self, candidate_id: str, status: str) -> Tuple[bool, Optional[str]]:
        """
        Update a candidate's processing status.
        
        Args:
            candidate_id: Candidate's unique identifier
            status: New status ('processing', 'completed', 'failed')
            
        Returns:
            Tuple of (success, error_message)
            - success: True if updated, False otherwise
            - error_message: None if successful, error description if failed
        """
        try:
            candidate = Candidate.query.get(candidate_id)
            
            if not candidate:
                return False, f"Candidate with ID {candidate_id} not found"
            
            # Validate status
            valid_statuses = ['processing', 'completed', 'failed']
            if status not in valid_statuses:
                return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            
            candidate.status = status
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update candidate status: {str(e)}"
    
    def save_uploaded_file(self, file: FileStorage) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Save an uploaded file to the upload folder with a secure filename.
        
        Args:
            file: Uploaded file from request
            
        Returns:
            Tuple of (file_path, filename, error_message)
            - file_path: Path where file was saved
            - filename: Secure filename used
            - error_message: None if successful, error description if failed
        """
        try:
            if not file or not file.filename:
                return None, None, "No file provided"
            
            # Validate filename format
            is_valid, error = self.file_validator.validate_file_format(file.filename)
            if not is_valid:
                return None, None, error
            
            # Generate secure filename
            secure_name = self.file_validator.generate_secure_filename(file.filename)
            
            # Save file
            file_path = os.path.join(self.upload_folder, secure_name)
            file.save(file_path)
            
            return file_path, secure_name, None
            
        except Exception as e:
            return None, None, f"Failed to save file: {str(e)}"
    
    def delete_file(self, file_path: str) -> None:
        """
        Delete a file from the filesystem.
        
        Args:
            file_path: Path to the file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Failed to delete file {file_path}: {str(e)}")
    
    def delete_candidate(self, candidate_id: str) -> Tuple[bool, Optional[str]]:
        """
        Delete a candidate permanently from database.
        Also deletes all related match results (cascade delete).
        
        Args:
            candidate_id: Candidate's unique identifier
            
        Returns:
            Tuple of (success, error_message)
            - success: True if deleted, False otherwise
            - error_message: None if successful, error description if failed
        """
        try:
            candidate = Candidate.query.get(candidate_id)
            
            if not candidate:
                return False, f"Candidate with ID {candidate_id} not found"
            
            # Delete the candidate (cascade will handle match_results)
            db.session.delete(candidate)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete candidate: {str(e)}"
