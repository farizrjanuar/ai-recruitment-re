"""
Job Service

This service provides business logic for job position management including
job creation, retrieval, updates, and job description processing using NLP.
"""

import spacy
from typing import Dict, List, Optional, Tuple

from extensions import db
from models.job_position import JobPosition


class JobService:
    """
    Service for managing job position operations and job description processing.
    
    Orchestrates:
    - Job position CRUD operations
    - Job description NLP processing
    - Job requirement extraction
    """
    
    def __init__(self):
        """Initialize the Job Service with spaCy NLP model."""
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
    
    def process_job_description(self, description: str) -> Dict:
        """
        Process job description using NLP to extract key requirements.
        
        Uses spaCy to:
        - Extract key skills and technologies mentioned
        - Identify experience requirements
        - Extract education requirements
        
        Args:
            description: Job description text
            
        Returns:
            dict: Processed job data with extracted requirements
        """
        try:
            # Process text with spaCy
            doc = self.nlp(description)
            
            # Extract entities and key terms
            extracted_skills = []
            experience_mentions = []
            education_mentions = []
            
            # Common skill-related keywords to look for
            skill_keywords = {
                'python', 'java', 'javascript', 'react', 'angular', 'vue',
                'node', 'django', 'flask', 'spring', 'sql', 'nosql',
                'mongodb', 'postgresql', 'mysql', 'aws', 'azure', 'gcp',
                'docker', 'kubernetes', 'git', 'ci/cd', 'agile', 'scrum',
                'machine learning', 'ai', 'data science', 'analytics'
            }
            
            # Experience-related patterns
            experience_patterns = ['years', 'experience', 'year']
            
            # Education-related patterns
            education_patterns = ['bachelor', 'master', 'phd', 'degree', 'diploma']
            
            # Extract skills from text
            text_lower = description.lower()
            for skill in skill_keywords:
                if skill in text_lower:
                    extracted_skills.append(skill.title())
            
            # Extract experience mentions
            for token in doc:
                if any(pattern in token.text.lower() for pattern in experience_patterns):
                    # Get surrounding context
                    start = max(0, token.i - 3)
                    end = min(len(doc), token.i + 4)
                    context = doc[start:end].text
                    experience_mentions.append(context)
            
            # Extract education mentions
            for token in doc:
                if any(pattern in token.text.lower() for pattern in education_patterns):
                    # Get surrounding context
                    start = max(0, token.i - 2)
                    end = min(len(doc), token.i + 3)
                    context = doc[start:end].text
                    education_mentions.append(context)
            
            return {
                'extracted_skills': list(set(extracted_skills)),
                'experience_mentions': experience_mentions[:3],  # Top 3
                'education_mentions': education_mentions[:3]  # Top 3
            }
            
        except Exception as e:
            # Return empty results if processing fails
            return {
                'extracted_skills': [],
                'experience_mentions': [],
                'education_mentions': [],
                'processing_error': str(e)
            }
    
    def create_job(self, job_data: Dict, created_by: str = None) -> Tuple[Optional[JobPosition], Optional[str]]:
        """
        Create a new job position.
        
        Args:
            job_data: Dictionary containing job information
            created_by: User ID of the creator (deprecated, kept for compatibility)
            
        Returns:
            Tuple of (job_instance, error_message)
            - job_instance: Created JobPosition object or None if failed
            - error_message: None if successful, error description if failed
        """
        try:
            # Validate required fields
            title = job_data.get('title', '').strip()
            description = job_data.get('description', '').strip()
            
            if not title:
                return None, "Job title is required"
            
            if not description:
                return None, "Job description is required"
            
            # Process job description to extract additional insights
            processed_data = self.process_job_description(description)
            
            # Create new job position instance (without created_by)
            job = JobPosition(
                title=title,
                description=description
            )
            
            # Set skills (combine provided skills with extracted ones)
            required_skills = job_data.get('required_skills', [])
            preferred_skills = job_data.get('preferred_skills', [])
            
            # Add extracted skills to preferred if not already in required
            extracted_skills = processed_data.get('extracted_skills', [])
            for skill in extracted_skills:
                if skill not in required_skills and skill not in preferred_skills:
                    preferred_skills.append(skill)
            
            job.set_required_skills(required_skills)
            job.set_preferred_skills(preferred_skills)
            
            # Set experience and education requirements
            job.min_experience_years = job_data.get('min_experience_years', 0)
            job.education_level = job_data.get('education_level')
            job.is_active = job_data.get('is_active', True)
            
            # Save to database
            db.session.add(job)
            db.session.commit()
            
            return job, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create job position: {str(e)}"
    
    def get_job(self, job_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Retrieve a job position by ID.
        
        Args:
            job_id: Job position's unique identifier
            
        Returns:
            Tuple of (job_dict, error_message)
            - job_dict: Job position data or None if not found
            - error_message: None if successful, error description if failed
        """
        try:
            job = JobPosition.query.get(job_id)
            
            if not job:
                return None, f"Job position with ID {job_id} not found"
            
            return job.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to retrieve job position: {str(e)}"
    
    def list_jobs(self, include_inactive: bool = False) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all job positions.
        
        Args:
            include_inactive: Whether to include inactive job positions
            
        Returns:
            Tuple of (jobs_list, error_message)
            - jobs_list: List of job position dictionaries
            - error_message: None if successful, error description if failed
        """
        try:
            # Build query
            query = JobPosition.query
            
            # Filter by active status if needed
            if not include_inactive:
                query = query.filter_by(is_active=True)
            
            # Order by creation date (newest first)
            jobs = query.order_by(JobPosition.created_at.desc()).all()
            
            # Convert to dictionaries
            jobs_list = [job.to_dict() for job in jobs]
            
            return jobs_list, None
            
        except Exception as e:
            return None, f"Failed to list job positions: {str(e)}"
    
    def update_job(self, job_id: str, job_data: Dict, user_id: str = None) -> Tuple[Optional[JobPosition], Optional[str]]:
        """
        Update an existing job position.
        
        Args:
            job_id: Job position's unique identifier
            job_data: Dictionary containing fields to update
            user_id: User ID making the update (deprecated, kept for compatibility)
            
        Returns:
            Tuple of (job_instance, error_message)
            - job_instance: Updated JobPosition object or None if failed
            - error_message: None if successful, error description if failed
        """
        try:
            job = JobPosition.query.get(job_id)
            
            if not job:
                return None, f"Job position with ID {job_id} not found"
            
            # Update fields if provided
            if 'title' in job_data:
                title = job_data['title'].strip()
                if not title:
                    return None, "Job title cannot be empty"
                job.title = title
            
            if 'description' in job_data:
                description = job_data['description'].strip()
                if not description:
                    return None, "Job description cannot be empty"
                job.description = description
            
            if 'required_skills' in job_data:
                job.set_required_skills(job_data['required_skills'])
            
            if 'preferred_skills' in job_data:
                job.set_preferred_skills(job_data['preferred_skills'])
            
            if 'min_experience_years' in job_data:
                job.min_experience_years = job_data['min_experience_years']
            
            if 'education_level' in job_data:
                job.education_level = job_data['education_level']
            
            if 'is_active' in job_data:
                job.is_active = job_data['is_active']
            
            # Save changes
            db.session.commit()
            
            return job, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update job position: {str(e)}"
    
    def deactivate_job(self, job_id: str) -> Tuple[bool, Optional[str]]:
        """
        Deactivate a job position (soft delete).
        
        Args:
            job_id: Job position's unique identifier
            
        Returns:
            Tuple of (success, error_message)
            - success: True if deactivated, False otherwise
            - error_message: None if successful, error description if failed
        """
        try:
            job = JobPosition.query.get(job_id)
            
            if not job:
                return False, f"Job position with ID {job_id} not found"
            
            job.deactivate()
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to deactivate job position: {str(e)}"
    
    def activate_job(self, job_id: str) -> Tuple[bool, Optional[str]]:
        """
        Activate a job position.
        
        Args:
            job_id: Job position's unique identifier
            
        Returns:
            Tuple of (success, error_message)
            - success: True if activated, False otherwise
            - error_message: None if successful, error description if failed
        """
        try:
            job = JobPosition.query.get(job_id)
            
            if not job:
                return False, f"Job position with ID {job_id} not found"
            
            job.activate()
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to activate job position: {str(e)}"
    
    def delete_job(self, job_id: str) -> Tuple[bool, Optional[str]]:
        """
        Delete a job position permanently from database.
        Also deletes all related match results (cascade delete).
        
        Args:
            job_id: Job position's unique identifier
            
        Returns:
            Tuple of (success, error_message)
            - success: True if deleted, False otherwise
            - error_message: None if successful, error description if failed
        """
        try:
            job = JobPosition.query.get(job_id)
            
            if not job:
                return False, f"Job position with ID {job_id} not found"
            
            # Delete the job (cascade will handle match_results)
            db.session.delete(job)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete job position: {str(e)}"
