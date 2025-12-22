"""
MatchResult model for storing candidate-job matching scores and analysis.
"""

import uuid
from datetime import datetime
from extensions import db


class MatchResult(db.Model):
    """
    MatchResult model representing the compatibility analysis between a candidate and job position.
    Stores overall match score and breakdown of individual scoring components.
    """
    
    __tablename__ = 'match_results'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    candidate_id = db.Column(db.String(36), db.ForeignKey('candidates.id'), nullable=False, index=True)
    job_id = db.Column(db.String(36), db.ForeignKey('job_positions.id'), nullable=False, index=True)
    
    # Match scores (0-100)
    match_score = db.Column(db.Float, nullable=False, index=True)  # Overall match score
    skill_match_score = db.Column(db.Float, nullable=False)  # Skills compatibility score
    experience_match_score = db.Column(db.Float, nullable=False)  # Experience level score
    education_match_score = db.Column(db.Float, nullable=False)  # Education level score
    
    # Qualification status
    status = db.Column(db.String(30), nullable=False, index=True)
    # Status values: 'Qualified', 'Potentially Qualified', 'Not Qualified'
    
    # Screening notes and reasoning
    screening_notes = db.Column(db.Text)
    
    # Timestamp
    calculated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Composite index for efficient queries
    __table_args__ = (
        db.Index('idx_job_match_score', 'job_id', 'match_score'),
        db.Index('idx_candidate_match_score', 'candidate_id', 'match_score'),
    )
    
    def __init__(self, candidate_id, job_id, match_score, skill_match_score, 
                 experience_match_score, education_match_score, status, screening_notes=None):
        """
        Initialize a new MatchResult instance.
        
        Args:
            candidate_id: ID of the candidate
            job_id: ID of the job position
            match_score: Overall match score (0-100)
            skill_match_score: Skills match score (0-100)
            experience_match_score: Experience match score (0-100)
            education_match_score: Education match score (0-100)
            status: Qualification status
            screening_notes: Optional notes explaining the match result
        """
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.match_score = match_score
        self.skill_match_score = skill_match_score
        self.experience_match_score = experience_match_score
        self.education_match_score = education_match_score
        self.status = status
        self.screening_notes = screening_notes
    
    def get_score_breakdown(self):
        """
        Get detailed breakdown of match scores.
        
        Returns:
            dict: Breakdown of all score components
        """
        return {
            'overall': self.match_score,
            'skill_match': self.skill_match_score,
            'experience_match': self.experience_match_score,
            'education_match': self.education_match_score
        }
    
    def is_qualified(self):
        """
        Check if candidate is qualified for the position.
        
        Returns:
            bool: True if status is 'Qualified'
        """
        return self.status == 'Qualified'
    
    def is_potentially_qualified(self):
        """
        Check if candidate is potentially qualified for the position.
        
        Returns:
            bool: True if status is 'Potentially Qualified'
        """
        return self.status == 'Potentially Qualified'
    
    def to_dict(self, include_candidate=False, include_job=False):
        """
        Convert MatchResult instance to dictionary representation.
        
        Args:
            include_candidate: Whether to include candidate information
            include_job: Whether to include job position information
            
        Returns:
            dict: Match result data
        """
        data = {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'match_score': round(self.match_score, 2),
            'skill_match': round(self.skill_match_score, 2),
            'experience_match': round(self.experience_match_score, 2),
            'education_match': round(self.education_match_score, 2),
            'status': self.status,
            'screening_notes': self.screening_notes,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None
        }
        
        if include_candidate and self.candidate:
            data['candidate'] = self.candidate.to_dict()
        
        if include_job and self.job_position:
            data['job'] = self.job_position.to_dict()
        
        return data
    
    def __repr__(self):
        """String representation of MatchResult."""
        return f'<MatchResult Candidate:{self.candidate_id[:8]} Job:{self.job_id[:8]} Score:{self.match_score:.1f}>'
