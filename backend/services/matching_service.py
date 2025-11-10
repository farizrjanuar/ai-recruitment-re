"""
Matching Service Module

This module provides business logic for calculating and managing
candidate-job matching scores and results.
"""

from typing import Dict, List, Optional
from models.candidate import Candidate
from models.job_position import JobPosition
from models.match_result import MatchResult
from ml.matching_engine import MatchingEngine
from extensions import db


class MatchingService:
    """
    Service class for managing candidate-job matching operations.
    
    Coordinates between the MatchingEngine (ML component) and the database
    to calculate, store, and retrieve match results.
    """
    
    def __init__(self):
        """Initialize the Matching Service with a MatchingEngine instance."""
        self.matching_engine = MatchingEngine()
    
    def calculate_matches(self, candidate_id: str) -> List[Dict]:
        """
        Calculate match scores for a candidate against all active job positions.
        
        Creates or updates MatchResult records in the database for each active job.
        
        Args:
            candidate_id: ID of the candidate to match
            
        Returns:
            list: List of match result dictionaries with job details
            
        Raises:
            ValueError: If candidate not found or has incomplete data
        """
        # Fetch candidate from database
        candidate = Candidate.query.get(candidate_id)
        
        if not candidate:
            raise ValueError(f"Candidate with ID {candidate_id} not found")
        
        if candidate.status != 'completed':
            raise ValueError(f"Candidate profile is not complete (status: {candidate.status})")
        
        # Get all active job positions
        active_jobs = JobPosition.query.filter_by(is_active=True).all()
        
        if not active_jobs:
            return []
        
        # Calculate matches for each job
        match_results = []
        
        for job in active_jobs:
            try:
                # Calculate single match
                match_result = self.calculate_single_match(candidate_id, job.id)
                match_results.append(match_result)
            except Exception as e:
                # Log error but continue with other jobs
                print(f"Error calculating match for job {job.id}: {str(e)}")
                continue
        
        # Sort by match score (descending)
        match_results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return match_results
    
    def calculate_single_match(self, candidate_id: str, job_id: str) -> Dict:
        """
        Calculate match score for a specific candidate-job pair.
        
        Creates or updates a MatchResult record in the database.
        
        Args:
            candidate_id: ID of the candidate
            job_id: ID of the job position
            
        Returns:
            dict: Match result with detailed breakdown
            
        Raises:
            ValueError: If candidate or job not found
        """
        # Fetch candidate and job from database
        candidate = Candidate.query.get(candidate_id)
        job = JobPosition.query.get(job_id)
        
        if not candidate:
            raise ValueError(f"Candidate with ID {candidate_id} not found")
        
        if not job:
            raise ValueError(f"Job position with ID {job_id} not found")
        
        if candidate.status != 'completed':
            raise ValueError(f"Candidate profile is not complete (status: {candidate.status})")
        
        # Convert to dictionaries for matching engine
        candidate_dict = candidate.to_dict()
        job_dict = job.to_dict()
        
        # Calculate match scores using ML engine
        match_scores = self.matching_engine.calculate_match_score(
            candidate_dict,
            job_dict
        )
        
        # Screen candidate to determine qualification status
        status, screening_notes = self.matching_engine.screen_candidate(
            candidate_dict,
            job_dict,
            match_scores
        )
        
        # Check if match result already exists
        existing_match = MatchResult.query.filter_by(
            candidate_id=candidate_id,
            job_id=job_id
        ).first()
        
        if existing_match:
            # Update existing match result
            existing_match.match_score = match_scores['match_score']
            existing_match.skill_match_score = match_scores['skill_match_score']
            existing_match.experience_match_score = match_scores['experience_match_score']
            existing_match.education_match_score = match_scores['education_match_score']
            existing_match.status = status
            existing_match.screening_notes = screening_notes
            match_result = existing_match
        else:
            # Create new match result
            match_result = MatchResult(
                candidate_id=candidate_id,
                job_id=job_id,
                match_score=match_scores['match_score'],
                skill_match_score=match_scores['skill_match_score'],
                experience_match_score=match_scores['experience_match_score'],
                education_match_score=match_scores['education_match_score'],
                status=status,
                screening_notes=screening_notes
            )
            db.session.add(match_result)
        
        # Commit to database
        db.session.commit()
        
        # Return match result with job details
        result_dict = match_result.to_dict()
        result_dict['job_title'] = job.title
        result_dict['job_description'] = job.description
        
        return result_dict
    
    def get_candidates_for_job(
        self, 
        job_id: str, 
        min_score: Optional[float] = None,
        status_filter: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get ranked list of candidates for a specific job position.
        
        Retrieves match results from database with optional filtering.
        
        Args:
            job_id: ID of the job position
            min_score: Minimum match score threshold (0-100)
            status_filter: Filter by qualification status 
                          ('Qualified', 'Potentially Qualified', 'Not Qualified', or 'all')
            limit: Maximum number of results to return
            
        Returns:
            list: List of candidate match results sorted by score (descending)
            
        Raises:
            ValueError: If job not found
        """
        # Verify job exists
        job = JobPosition.query.get(job_id)
        
        if not job:
            raise ValueError(f"Job position with ID {job_id} not found")
        
        # Build query
        query = MatchResult.query.filter_by(job_id=job_id)
        
        # Apply filters
        if min_score is not None:
            query = query.filter(MatchResult.match_score >= min_score)
        
        if status_filter and status_filter.lower() != 'all':
            query = query.filter(MatchResult.status == status_filter)
        
        # Order by match score (descending)
        query = query.order_by(MatchResult.match_score.desc())
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        # Execute query
        match_results = query.all()
        
        # Convert to dictionaries with candidate details
        results = []
        for match in match_results:
            result_dict = match.to_dict()
            
            # Add candidate information
            candidate = Candidate.query.get(match.candidate_id)
            if candidate:
                result_dict['candidate_name'] = candidate.name
                result_dict['candidate_email'] = candidate.email
                result_dict['candidate_phone'] = candidate.phone
                result_dict['candidate_experience_years'] = candidate.total_experience_years
                result_dict['candidate_skills'] = candidate.get_skills()
            
            results.append(result_dict)
        
        return results
    
    def get_match_result(self, candidate_id: str, job_id: str) -> Optional[Dict]:
        """
        Get existing match result for a candidate-job pair.
        
        Args:
            candidate_id: ID of the candidate
            job_id: ID of the job position
            
        Returns:
            dict: Match result or None if not found
        """
        match_result = MatchResult.query.filter_by(
            candidate_id=candidate_id,
            job_id=job_id
        ).first()
        
        if not match_result:
            return None
        
        return match_result.to_dict()
    
    def get_candidate_matches(
        self, 
        candidate_id: str,
        min_score: Optional[float] = None
    ) -> List[Dict]:
        """
        Get all match results for a specific candidate.
        
        Args:
            candidate_id: ID of the candidate
            min_score: Minimum match score threshold (0-100)
            
        Returns:
            list: List of match results with job details
            
        Raises:
            ValueError: If candidate not found
        """
        # Verify candidate exists
        candidate = Candidate.query.get(candidate_id)
        
        if not candidate:
            raise ValueError(f"Candidate with ID {candidate_id} not found")
        
        # Build query
        query = MatchResult.query.filter_by(candidate_id=candidate_id)
        
        # Apply filter
        if min_score is not None:
            query = query.filter(MatchResult.match_score >= min_score)
        
        # Order by match score (descending)
        query = query.order_by(MatchResult.match_score.desc())
        
        # Execute query
        match_results = query.all()
        
        # Convert to dictionaries with job details
        results = []
        for match in match_results:
            result_dict = match.to_dict()
            
            # Add job information
            job = JobPosition.query.get(match.job_id)
            if job:
                result_dict['job_title'] = job.title
                result_dict['job_description'] = job.description
                result_dict['job_is_active'] = job.is_active
            
            results.append(result_dict)
        
        return results
