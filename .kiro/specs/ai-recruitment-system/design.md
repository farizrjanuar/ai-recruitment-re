# Design Document - AI Recruitment System

## Overview

The AI Recruitment System is built using a modern microservices-inspired architecture with a clear separation between frontend (React), backend API (Python/Flask), and AI/ML processing components. The system processes CV documents, extracts structured information using NLP, performs intelligent candidate-job matching using machine learning models, and provides an intuitive dashboard for HR users.

### Technology Stack

**Backend:**
- Python 3.9+
- Flask (REST API framework)
- Flask-JWT-Extended (authentication)
- Flask-CORS (cross-origin support)
- SQLAlchemy (ORM)
- SQLite (development) / PostgreSQL (production - free tier)

**AI/ML Libraries:**
- spaCy (NLP and text processing) - use small model (en_core_web_sm)
- scikit-learn (TF-IDF, cosine similarity, ML models)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- pandas (data manipulation)
- numpy (numerical operations)

**Frontend:**
- React 19.2
- Axios (HTTP client)
- React Router (navigation)
- Chart.js or Recharts (data visualization)

**Free Hosting Options:**
- Backend: Render.com (free tier), Railway.app (free tier), or PythonAnywhere
- Frontend: Vercel (free), Netlify (free), or GitHub Pages
- Database: Render PostgreSQL (free tier) or Railway PostgreSQL (free tier)
- File Storage: Local filesystem (backend) or Cloudinary (free tier for images)

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  React Frontend │
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP/REST
         │ (JWT Auth)
         ▼
┌─────────────────┐
│  Flask Backend  │
│   (Port 5000)   │
│                 │
│  ┌───────────┐  │
│  │ API Layer │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  Service  │  │
│  │   Layer   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ ML Engine │  │
│  └───────────┘  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
│    Database     │
└─────────────────┘
```

### Component Architecture

```
Backend Components:
├── app.py (Flask application entry point)
├── config.py (configuration management)
├── models/ (database models)
│   ├── user.py
│   ├── candidate.py
│   ├── job_position.py
│   └── match_result.py
├── services/ (business logic)
│   ├── cv_parser_service.py
│   ├── candidate_service.py
│   ├── job_service.py
│   └── matching_service.py
├── ml/ (AI/ML components)
│   ├── text_extractor.py
│   ├── skill_analyzer.py
│   └── matching_engine.py
├── routes/ (API endpoints)
│   ├── auth_routes.py
│   ├── candidate_routes.py
│   ├── job_routes.py
│   └── dashboard_routes.py
└── utils/ (helper functions)
    ├── file_handler.py
    └── validators.py
```

## Components and Interfaces

### 1. API Layer

#### Authentication Endpoints

```
POST /api/auth/register
Request: { "email": string, "password": string, "role": string }
Response: { "message": string, "user_id": string }

POST /api/auth/login
Request: { "email": string, "password": string }
Response: { "access_token": string, "user": { "id": string, "email": string, "role": string } }

POST /api/auth/refresh
Headers: { "Authorization": "Bearer <token>" }
Response: { "access_token": string }
```

#### Candidate Management Endpoints

```
POST /api/candidates/upload
Headers: { "Authorization": "Bearer <token>" }
Request: multipart/form-data { "cv_file": File }
Response: { 
  "candidate_id": string,
  "status": "processing" | "completed" | "failed",
  "message": string
}

GET /api/candidates
Headers: { "Authorization": "Bearer <token>" }
Query: ?page=1&limit=20&job_id=<optional>
Response: {
  "candidates": [
    {
      "id": string,
      "name": string,
      "email": string,
      "skills": string[],
      "experience_years": number,
      "created_at": timestamp
    }
  ],
  "total": number,
  "page": number
}

GET /api/candidates/:id
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "id": string,
  "name": string,
  "email": string,
  "phone": string,
  "education": object[],
  "experience": object[],
  "skills": object[],
  "certifications": string[],
  "raw_text": string,
  "created_at": timestamp
}
```

#### Job Position Endpoints

```
POST /api/jobs
Headers: { "Authorization": "Bearer <token>" }
Request: {
  "title": string,
  "description": string,
  "required_skills": string[],
  "preferred_skills": string[],
  "min_experience_years": number,
  "education_level": string
}
Response: { "job_id": string, "message": string }

GET /api/jobs
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "jobs": [
    {
      "id": string,
      "title": string,
      "description": string,
      "required_skills": string[],
      "candidate_count": number,
      "created_at": timestamp
    }
  ]
}

GET /api/jobs/:id
Headers: { "Authorization": "Bearer <token>" }
Response: { <full job details> }

PUT /api/jobs/:id
Headers: { "Authorization": "Bearer <token>" }
Request: { <job fields to update> }
Response: { "message": string }
```

#### Matching Endpoints

```
POST /api/matching/calculate/:candidate_id
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "candidate_id": string,
  "matches": [
    {
      "job_id": string,
      "job_title": string,
      "match_score": number,
      "skill_match": number,
      "experience_match": number,
      "education_match": number,
      "status": "Qualified" | "Potentially Qualified" | "Not Qualified"
    }
  ]
}

GET /api/matching/job/:job_id
Headers: { "Authorization": "Bearer <token>" }
Query: ?min_score=0&status=all
Response: {
  "job_id": string,
  "job_title": string,
  "candidates": [
    {
      "candidate_id": string,
      "name": string,
      "match_score": number,
      "status": string,
      "breakdown": object
    }
  ]
}
```

#### Dashboard Endpoints

```
GET /api/dashboard/stats
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "total_candidates": number,
  "total_jobs": number,
  "avg_match_score": number,
  "qualified_candidates": number,
  "recent_uploads": number
}

GET /api/dashboard/analytics
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "skill_distribution": { "skill_name": count },
  "experience_distribution": { "range": count },
  "match_score_distribution": { "range": count }
}
```

### 2. Service Layer

#### CV Parser Service

**Responsibilities:**
- Accept uploaded CV files
- Extract text from PDF, DOCX, TXT formats
- Parse structured information (name, email, phone, education, experience, skills)
- Create candidate profiles

**Key Methods:**
```python
class CVParserService:
    def parse_cv(file_path: str, file_type: str) -> dict
    def extract_text(file_path: str, file_type: str) -> str
    def extract_contact_info(text: str) -> dict
    def extract_education(text: str) -> list
    def extract_experience(text: str) -> list
    def extract_skills(text: str) -> list
```

#### Candidate Service

**Responsibilities:**
- Manage candidate CRUD operations
- Coordinate CV parsing and profile creation
- Retrieve candidate data with filtering

**Key Methods:**
```python
class CandidateService:
    def create_candidate(cv_file) -> str
    def get_candidate(candidate_id: str) -> dict
    def list_candidates(filters: dict, pagination: dict) -> list
    def update_candidate(candidate_id: str, data: dict) -> bool
```

#### Job Service

**Responsibilities:**
- Manage job position CRUD operations
- Process job descriptions with NLP
- Extract job requirements

**Key Methods:**
```python
class JobService:
    def create_job(job_data: dict) -> str
    def get_job(job_id: str) -> dict
    def list_jobs() -> list
    def update_job(job_id: str, data: dict) -> bool
    def deactivate_job(job_id: str) -> bool
```

#### Matching Service

**Responsibilities:**
- Calculate match scores between candidates and jobs
- Apply screening criteria
- Rank candidates for positions

**Key Methods:**
```python
class MatchingService:
    def calculate_matches(candidate_id: str) -> list
    def calculate_single_match(candidate_id: str, job_id: str) -> dict
    def get_candidates_for_job(job_id: str, filters: dict) -> list
    def apply_screening(candidate: dict, job: dict) -> str
```

### 3. ML Engine

#### Text Extractor

**Purpose:** Extract and preprocess text from various document formats

**Implementation:**
```python
class TextExtractor:
    def extract_from_pdf(file_path: str) -> str
        # Use PyPDF2 to extract text from PDF
    
    def extract_from_docx(file_path: str) -> str
        # Use python-docx to extract text
    
    def extract_from_txt(file_path: str) -> str
        # Read plain text file
    
    def clean_text(text: str) -> str
        # Remove special characters, normalize whitespace
```

#### Skill Analyzer

**Purpose:** Analyze and categorize skills from CV text using NLP

**Implementation:**
```python
class SkillAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_categories = self._load_skill_taxonomy()
    
    def analyze_skills(text: str) -> list
        # Extract skills using NER and pattern matching
        # Categorize skills (programming, frameworks, tools, soft skills)
        # Return structured skill data
    
    def calculate_skill_score(skill: str, context: str) -> float
        # Analyze skill proficiency based on context
        # Return score 0-100
    
    def extract_experience_years(text: str, skill: str) -> int
        # Find years of experience for specific skill
```

**Skill Taxonomy Structure:**
```python
{
    "programming_languages": ["Python", "JavaScript", "Java", "C++", ...],
    "frameworks": ["React", "Flask", "Django", "Spring", ...],
    "databases": ["PostgreSQL", "MongoDB", "MySQL", ...],
    "tools": ["Git", "Docker", "Kubernetes", ...],
    "soft_skills": ["Leadership", "Communication", "Problem Solving", ...]
}
```

#### Matching Engine

**Purpose:** Calculate compatibility scores between candidates and job positions

**Implementation:**
```python
class MatchingEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)
    
    def calculate_match_score(candidate: dict, job: dict) -> dict
        # Calculate overall match score (0-100)
        # Return breakdown: skill_match, experience_match, education_match
    
    def _calculate_skill_match(candidate_skills: list, job_skills: list) -> float
        # Use TF-IDF and cosine similarity
        # Weight required vs preferred skills
    
    def _calculate_experience_match(candidate_exp: int, required_exp: int) -> float
        # Compare years of experience
    
    def _calculate_education_match(candidate_edu: str, required_edu: str) -> float
        # Compare education levels
    
    def screen_candidate(candidate: dict, job: dict) -> str
        # Return "Qualified", "Potentially Qualified", or "Not Qualified"
```

**Matching Algorithm:**
1. **Skill Matching (50% weight):**
   - Convert candidate skills and job requirements to TF-IDF vectors
   - Calculate cosine similarity
   - Apply bonus for exact matches on required skills
   - Score: 0-100

2. **Experience Matching (30% weight):**
   - Compare candidate's total experience with job requirement
   - Score = min(100, (candidate_exp / required_exp) * 100)

3. **Education Matching (20% weight):**
   - Map education levels to numeric scale
   - Compare candidate education with requirement
   - Score based on meeting or exceeding requirement

4. **Final Score:**
   - Weighted average of all components
   - Round to integer (0-100)

## Data Models

### User Model

```python
class User:
    id: UUID (primary key)
    email: String (unique, not null)
    password_hash: String (not null)
    role: Enum["Admin", "HR"] (not null)
    created_at: DateTime
    updated_at: DateTime
```

### Candidate Model

```python
class Candidate:
    id: UUID (primary key)
    name: String
    email: String (unique)
    phone: String
    raw_cv_text: Text
    education: JSON  # [{ "degree": str, "institution": str, "year": int }]
    experience: JSON  # [{ "title": str, "company": str, "duration": str, "description": str }]
    skills: JSON  # [{ "name": str, "category": str, "score": float, "years": int }]
    certifications: JSON  # [str]
    total_experience_years: Integer
    status: Enum["processing", "completed", "failed"]
    created_at: DateTime
    updated_at: DateTime
```

### JobPosition Model

```python
class JobPosition:
    id: UUID (primary key)
    title: String (not null)
    description: Text (not null)
    required_skills: JSON  # [str]
    preferred_skills: JSON  # [str]
    min_experience_years: Integer
    education_level: String
    is_active: Boolean (default True)
    created_by: UUID (foreign key -> User)
    created_at: DateTime
    updated_at: DateTime
```

### MatchResult Model

```python
class MatchResult:
    id: UUID (primary key)
    candidate_id: UUID (foreign key -> Candidate)
    job_id: UUID (foreign key -> JobPosition)
    match_score: Float (0-100)
    skill_match_score: Float
    experience_match_score: Float
    education_match_score: Float
    status: Enum["Qualified", "Potentially Qualified", "Not Qualified"]
    screening_notes: Text
    calculated_at: DateTime
```

### Database Indexes

```sql
CREATE INDEX idx_candidate_email ON candidates(email);
CREATE INDEX idx_candidate_status ON candidates(status);
CREATE INDEX idx_job_active ON job_positions(is_active);
CREATE INDEX idx_match_job ON match_results(job_id, match_score DESC);
CREATE INDEX idx_match_candidate ON match_results(candidate_id);
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_INVALID_CREDENTIALS | 401 | Invalid email or password |
| AUTH_TOKEN_EXPIRED | 401 | JWT token has expired |
| AUTH_TOKEN_INVALID | 401 | JWT token is malformed or invalid |
| AUTH_INSUFFICIENT_PERMISSIONS | 403 | User lacks required permissions |
| FILE_TOO_LARGE | 400 | Uploaded file exceeds 5MB limit |
| FILE_INVALID_FORMAT | 400 | File format not supported |
| FILE_UNREADABLE | 400 | Cannot extract text from file |
| CANDIDATE_NOT_FOUND | 404 | Candidate ID does not exist |
| JOB_NOT_FOUND | 404 | Job position ID does not exist |
| VALIDATION_ERROR | 400 | Request data validation failed |
| PROCESSING_ERROR | 500 | Error during CV processing |
| DATABASE_ERROR | 500 | Database operation failed |

### Exception Handling Strategy

```python
# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, ValidationError):
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": str(e)}}), 400
    elif isinstance(e, NotFoundError):
        return jsonify({"error": {"code": e.code, "message": str(e)}}), 404
    else:
        # Log unexpected errors
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}}), 500

# Service-level error handling
class CVParserService:
    def parse_cv(self, file_path, file_type):
        try:
            text = self.extract_text(file_path, file_type)
            if not text or len(text) < 50:
                raise ValidationError("CV file does not contain sufficient text")
            return self._parse_content(text)
        except Exception as e:
            raise ProcessingError(f"Failed to parse CV: {str(e)}")
```

## Testing Strategy

### Unit Testing

**Scope:** Test individual components in isolation

**Tools:** pytest, unittest.mock

**Coverage:**
- ML Engine components (text extraction, skill analysis, matching algorithms)
- Service layer methods
- Utility functions
- Data model validations

**Example Test Cases:**
```python
def test_extract_text_from_pdf():
    # Test PDF text extraction
    
def test_skill_analyzer_categorization():
    # Test skill categorization accuracy
    
def test_matching_score_calculation():
    # Test match score algorithm with known inputs
    
def test_candidate_service_create():
    # Test candidate creation with mocked dependencies
```

### Integration Testing

**Scope:** Test component interactions and API endpoints

**Tools:** pytest, Flask test client

**Coverage:**
- API endpoint responses
- Database operations
- Service layer integration
- Authentication flow

**Example Test Cases:**
```python
def test_upload_cv_endpoint():
    # Test complete CV upload flow
    
def test_calculate_matches_integration():
    # Test matching service with real database
    
def test_jwt_authentication():
    # Test protected endpoint access
```

### End-to-End Testing

**Scope:** Test complete user workflows

**Coverage:**
- CV upload → parsing → profile creation → matching
- Job creation → candidate matching → results retrieval
- HR dashboard data flow

### Performance Testing

**Metrics:**
- CV processing time: < 10 seconds per file
- Match calculation: < 2 seconds for 100 candidates
- API response time: < 500ms for standard queries
- Database query time: < 100ms with proper indexing

## Security Considerations

1. **Authentication:**
   - JWT tokens with 24-hour expiration
   - Secure password hashing with bcrypt (10+ rounds)
   - Token refresh mechanism

2. **Authorization:**
   - Role-based access control (Admin, HR)
   - Endpoint-level permission checks

3. **Input Validation:**
   - File type and size validation
   - Request data sanitization
   - SQL injection prevention (using ORM)

4. **Data Protection:**
   - HTTPS for all communications
   - Sensitive data encryption at rest
   - CORS configuration for frontend origin

5. **File Upload Security:**
   - Virus scanning (optional, using ClamAV)
   - Secure file storage with unique names
   - Temporary file cleanup

## Deployment Architecture (Zero Cost)

```
Free Tier Production Environment:
├── Frontend (Vercel - FREE)
│   └── React build artifacts
│   └── Automatic deployments from GitHub
├── Backend (Render.com - FREE or Railway.app - FREE)
│   ├── Flask application (Gunicorn)
│   ├── Environment variables
│   ├── File storage (local filesystem)
│   └── Auto-sleep after 15 min inactivity (Render free tier)
└── Database (Render PostgreSQL - FREE or Railway - FREE)
    └── PostgreSQL instance (90 days retention on Render)
    └── Alternative: SQLite for development
```

### Free Tier Limitations & Solutions

**Render.com Free Tier:**
- ✅ 750 hours/month (enough for 1 service)
- ⚠️ Sleeps after 15 min inactivity (cold start ~30s)
- ✅ 512MB RAM
- ✅ PostgreSQL free tier (90 days, then expires - need to backup/restore)
- **Solution:** Accept cold starts, or use Railway as alternative

**Railway.app Free Tier:**
- ✅ $5 free credit/month
- ✅ No sleep time
- ✅ PostgreSQL included
- **Solution:** Monitor usage to stay within free credit

**Vercel Free Tier:**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Perfect for React frontend

**File Storage Strategy (Zero Cost):**
- Store uploaded CVs in backend filesystem
- Clean up old files after processing (keep only extracted data)
- Alternative: Cloudinary free tier (25 credits/month) if needed

### Environment Variables

```
FLASK_ENV=production
SECRET_KEY=<random-secret-key>
JWT_SECRET_KEY=<jwt-secret-key>
DATABASE_URL=postgresql://user:pass@host:port/dbname
# For Railway/Render, this is auto-provided
CORS_ORIGINS=https://your-app.vercel.app
MAX_FILE_SIZE=5242880
UPLOAD_FOLDER=/tmp/uploads
# Use SQLite for local dev
DATABASE_URL_DEV=sqlite:///recruitment.db
```

### Development Setup (Zero Cost)

```bash
# Local development uses SQLite
DATABASE_URL=sqlite:///recruitment.db

# Production uses free PostgreSQL
DATABASE_URL=<provided-by-render-or-railway>
```

## Cost Optimization Strategies

1. **Database:**
   - Use SQLite for development and testing
   - Migrate to free PostgreSQL (Render/Railway) for production
   - Implement data cleanup policies (delete old CVs after 30 days)

2. **File Storage:**
   - Store files temporarily, delete after processing
   - Keep only extracted JSON data in database
   - Use compression for stored text data

3. **ML Models:**
   - Use lightweight spaCy model (en_core_web_sm - 12MB)
   - Avoid heavy models like BERT (requires more RAM)
   - Use scikit-learn (lightweight, efficient)

4. **API Optimization:**
   - Implement pagination to reduce data transfer
   - Use JSON compression
   - Cache frequently accessed data in-memory

5. **Monitoring:**
   - Use free tier monitoring (Render dashboard, Railway dashboard)
   - Implement basic logging (no paid services)

## Future Enhancements (When Budget Available)

1. **Advanced ML Models:**
   - BERT-based semantic matching
   - Neural network for scoring
   - Resume quality assessment

2. **Additional Features:**
   - Email notifications (SendGrid free tier: 100 emails/day)
   - Interview scheduling
   - Candidate communication portal
   - Resume builder

3. **Performance Optimization:**
   - Caching layer (Redis free tier)
   - Async processing (Celery)
   - CDN for file storage

4. **Analytics:**
   - Advanced reporting
   - Hiring funnel metrics
   - Diversity analytics
