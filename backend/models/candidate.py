"""
Candidate model for storing parsed CV data and candidate profiles.
"""

import uuid
import json
from datetime import datetime
from extensions import db


class Candidate(db.Model):
    """
    Candidate model representing a job applicant with extracted CV information.
    Stores structured data from parsed CVs including education, experience, and skills.
    """
    
    __tablename__ = 'candidates'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Contact information
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    phone = db.Column(db.String(50))
    
    # Raw CV text
    raw_cv_text = db.Column(db.Text)
    
    # Structured data stored as JSON
    education = db.Column(db.JSON)  # [{"degree": str, "institution": str, "year": int}]
    experience = db.Column(db.JSON)  # [{"title": str, "company": str, "duration": str, "description": str}]
    skills = db.Column(db.JSON)  # [{"name": str, "category": str, "score": float, "years": int}]
    certifications = db.Column(db.JSON)  # [str]
    
    # Calculated fields
    total_experience_years = db.Column(db.Integer, default=0)
    
    # Processing status
    status = db.Column(db.String(20), nullable=False, default='processing', index=True)
    # Status values: 'processing', 'completed', 'failed'
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    match_results = db.relationship('MatchResult', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """
        Initialize a new Candidate instance.
        
        Args:
            **kwargs: Candidate attributes
        """
        super(Candidate, self).__init__(**kwargs)
        # Initialize JSON fields as empty lists if not provided
        if self.education is None:
            self.education = []
        if self.experience is None:
            self.experience = []
        if self.skills is None:
            self.skills = []
        if self.certifications is None:
            self.certifications = []
    
    def set_education(self, education_list):
        """
        Set education data with proper serialization.
        
        Args:
            education_list: List of education dictionaries
        """
        self.education = education_list if education_list else []
    
    def get_education(self):
        """
        Get education data with proper deserialization.
        
        Returns:
            list: Education data
        """
        return self.education if self.education else []
    
    def set_experience(self, experience_list):
        """
        Set experience data with proper serialization.
        
        Args:
            experience_list: List of experience dictionaries
        """
        self.experience = experience_list if experience_list else []
    
    def get_experience(self):
        """
        Get experience data with proper deserialization.
        
        Returns:
            list: Experience data
        """
        return self.experience if self.experience else []
    
    def set_skills(self, skills_list):
        """
        Set skills data with proper serialization.
        
        Args:
            skills_list: List of skill dictionaries
        """
        self.skills = skills_list if skills_list else []
    
    def get_skills(self):
        """
        Get skills data with proper deserialization.
        
        Returns:
            list: Skills data
        """
        return self.skills if self.skills else []
    
    def set_certifications(self, certifications_list):
        """
        Set certifications data with proper serialization.
        
        Args:
            certifications_list: List of certification strings
        """
        self.certifications = certifications_list if certifications_list else []
    
    def get_certifications(self):
        """
        Get certifications data with proper deserialization.
        
        Returns:
            list: Certifications data
        """
        return self.certifications if self.certifications else []
    
    def to_dict(self, include_raw_text=False):
        """
        Convert Candidate instance to dictionary representation.
        
        Args:
            include_raw_text: Whether to include raw CV text in output
            
        Returns:
            dict: Candidate data
        """
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'education': self.get_education(),
            'experience': self.get_experience(),
            'skills': self.get_skills(),
            'certifications': self.get_certifications(),
            'total_experience_years': self.total_experience_years,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_raw_text:
            data['raw_cv_text'] = self.raw_cv_text
        
        return data
    
    def __repr__(self):
        """String representation of Candidate."""
        return f'<Candidate {self.name} ({self.email})>'
