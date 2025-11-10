"""
User model for authentication and authorization.
"""

import uuid
from datetime import datetime
from extensions import db
import bcrypt


class User(db.Model):
    """
    User model for HR users and administrators.
    Handles authentication and role-based access control.
    """
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication fields
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role-based access control
    role = db.Column(db.String(20), nullable=False, default='HR')  # 'Admin' or 'HR'
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_positions = db.relationship('JobPosition', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, password, role='HR'):
        """
        Initialize a new User instance.
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            role: User role ('Admin' or 'HR')
        """
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        """
        Hash and set the user's password using bcrypt.
        
        Args:
            password: Plain text password to hash
        """
        # Generate salt and hash password with bcrypt (10 rounds minimum)
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """
        Verify a password against the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """
        Convert User instance to dictionary representation.
        
        Returns:
            dict: User data (excluding password_hash)
        """
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of User."""
        return f'<User {self.email} ({self.role})>'
