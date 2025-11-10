# Database Models

This directory contains all SQLAlchemy database models for the AI Recruitment System.

## Models Overview

### User Model (`user.py`)
- Handles authentication and authorization
- Fields: id, email, password_hash, role, timestamps
- Password hashing using bcrypt (12 rounds)
- Roles: 'Admin', 'HR'
- Relationships: One-to-many with JobPosition

### Candidate Model (`candidate.py`)
- Stores parsed CV data and candidate profiles
- Fields: id, name, email, phone, raw_cv_text, education (JSON), experience (JSON), skills (JSON), certifications (JSON), total_experience_years, status, timestamps
- Status values: 'processing', 'completed', 'failed'
- JSON serialization/deserialization methods for structured data
- Relationships: One-to-many with MatchResult

### JobPosition Model (`job_position.py`)
- Manages job openings and requirements
- Fields: id, title, description, required_skills (JSON), preferred_skills (JSON), min_experience_years, education_level, is_active, created_by (FK), timestamps
- Soft deletion via is_active flag
- Relationships: Many-to-one with User, One-to-many with MatchResult

### MatchResult Model (`match_result.py`)
- Stores candidate-job matching scores and analysis
- Fields: id, candidate_id (FK), job_id (FK), match_score, skill_match_score, experience_match_score, education_match_score, status, screening_notes, calculated_at
- Status values: 'Qualified', 'Potentially Qualified', 'Not Qualified'
- Composite indexes for efficient queries
- Relationships: Many-to-one with Candidate and JobPosition

## Database Indexes

The following indexes are created for performance optimization:

- `users.email` (unique)
- `candidates.email` (unique)
- `candidates.status`
- `job_positions.is_active`
- `match_results.candidate_id`
- `match_results.job_id`
- `match_results.match_score`
- `match_results.status`
- Composite: `(job_id, match_score)`
- Composite: `(candidate_id, match_score)`

## Database Initialization

To initialize the database and create tables:

```bash
# Initialize tables only
python init_db.py

# Initialize and seed with sample data
python init_db.py --seed

# Reset database (drop all tables and reinitialize)
python init_db.py --reset
```

## Sample Data

When seeding the database, the following sample data is created:

**Users:**
- Admin: admin@recruitment.com / admin123
- HR: hr@recruitment.com / hr123

**Job Positions:**
- Senior Python Developer
- Machine Learning Engineer
- Frontend Developer

**Candidates:**
- John Smith (Python Developer, 6 years experience)
- Sarah Johnson (ML Engineer, 4 years experience)
- Mike Chen (Frontend Developer, 3 years experience)

**Match Results:**
- 4 sample matches between candidates and jobs

## Usage Example

```python
from app import create_app, db
from models import User, Candidate, JobPosition, MatchResult

app = create_app()

with app.app_context():
    # Create a new user
    user = User(email='test@example.com', password='password123', role='HR')
    db.session.add(user)
    db.session.commit()
    
    # Query candidates
    candidates = Candidate.query.filter_by(status='completed').all()
    
    # Get match results for a job
    matches = MatchResult.query.filter_by(job_id=job_id).order_by(
        MatchResult.match_score.desc()
    ).all()
```
