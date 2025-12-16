"""
JobPosition model for managing job openings and requirements.
"""

import uuid
from datetime import datetime
from extensions import db


class JobPosition(db.Model):
    """
    JobPosition model representing a job opening with requirements and qualifications.
    Used for matching candidates to suitable positions.
    """
    
    __tablename__ = 'job_positions'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Job details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Skills requirements stored as JSON
    required_skills = db.Column(db.JSON)  # [str] - Must-have skills
    preferred_skills = db.Column(db.JSON)  # [str] - Nice-to-have skills
    
    # Experience and education requirements
    min_experience_years = db.Column(db.Integer, default=0)
    education_level = db.Column(db.String(100))  # e.g., "Bachelor's", "Master's", "PhD"
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    match_results = db.relationship('MatchResult', backref='job_position', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, title, description, **kwargs):
        """
        Initialize a new JobPosition instance.
        
        Args:
            title: Job title
            description: Job description
            **kwargs: Additional job attributes
        """
        self.title = title
        self.description = description
        
        # Initialize JSON fields as empty lists if not provided
        self.required_skills = kwargs.get('required_skills', [])
        self.preferred_skills = kwargs.get('preferred_skills', [])
        self.min_experience_years = kwargs.get('min_experience_years', 0)
        self.education_level = kwargs.get('education_level')
        self.is_active = kwargs.get('is_active', True)
    
    def set_required_skills(self, skills_list):
        """
        Set required skills with proper serialization.
        
        Args:
            skills_list: List of required skill strings
        """
        self.required_skills = skills_list if skills_list else []
    
    def get_required_skills(self):
        """
        Get required skills with proper deserialization.
        
        Returns:
            list: Required skills
        """
        return self.required_skills if self.required_skills else []
    
    def set_preferred_skills(self, skills_list):
        """
        Set preferred skills with proper serialization.
        
        Args:
            skills_list: List of preferred skill strings
        """
        self.preferred_skills = skills_list if skills_list else []
    
    def get_preferred_skills(self):
        """
        Get preferred skills with proper deserialization.
        
        Returns:
            list: Preferred skills
        """
        return self.preferred_skills if self.preferred_skills else []
    
    def activate(self):
        """Activate this job position."""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate this job position (soft delete)."""
        self.is_active = False
    
    def to_dict(self, include_creator=False):
        """
        Convert JobPosition instance to dictionary representation.
        
        Args:
            include_creator: Whether to include creator information (deprecated)
            
        Returns:
            dict: Job position data
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.get_required_skills(),
            'preferred_skills': self.get_preferred_skills(),
            'min_experience_years': self.min_experience_years,
            'education_level': self.education_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        return data
    
    def __repr__(self):
        """String representation of JobPosition."""
        status = "Active" if self.is_active else "Inactive"
        return f'<JobPosition {self.title} ({status})>'
