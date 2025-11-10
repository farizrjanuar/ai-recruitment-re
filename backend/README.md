# AI Recruitment System - Backend

Flask-based backend API for the AI Recruitment System with integrated ML/NLP capabilities.

## Project Structure

```
backend/
├── models/          # Database models (SQLAlchemy)
├── services/        # Business logic services
├── ml/              # Machine learning and NLP components
├── routes/          # API endpoints (Flask blueprints)
├── utils/           # Helper functions and utilities
├── uploads/         # Uploaded CV files (created automatically)
├── app.py           # Flask application entry point
├── config.py        # Configuration management
└── requirements.txt # Python dependencies
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- Set `SECRET_KEY` and `JWT_SECRET_KEY` to random secure strings
- Configure `DATABASE_URL` (SQLite for dev, PostgreSQL for production)
- Adjust other settings as needed

### 5. Run the Application

```bash
# Development mode
python app.py

# Or using Flask CLI
flask run
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Check API status
- `GET /` - API information

### Authentication (to be implemented)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh JWT token

### Candidates (to be implemented)
- `POST /api/candidates/upload` - Upload CV
- `GET /api/candidates` - List candidates
- `GET /api/candidates/:id` - Get candidate details

### Jobs (to be implemented)
- `POST /api/jobs` - Create job position
- `GET /api/jobs` - List job positions
- `GET /api/jobs/:id` - Get job details
- `PUT /api/jobs/:id` - Update job position

### Matching (to be implemented)
- `POST /api/matching/calculate/:candidate_id` - Calculate matches
- `GET /api/matching/job/:job_id` - Get candidates for job

### Dashboard (to be implemented)
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/analytics` - Get analytics data

## Development

### Database Migrations

The application automatically creates database tables on startup. For production, consider using Flask-Migrate for proper database migrations.

### Testing

Run tests (to be implemented):
```bash
pytest
```

## Deployment

### Free Hosting Options

**Backend:**
- Render.com (free tier)
- Railway.app (free tier)
- PythonAnywhere

**Database:**
- Render PostgreSQL (free tier)
- Railway PostgreSQL (free tier)

See deployment documentation for detailed instructions.

## Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-JWT-Extended 4.6.0** - JWT authentication
- **Flask-CORS 4.0.0** - Cross-origin support
- **spaCy 3.7.2** - NLP processing
- **scikit-learn 1.3.2** - Machine learning
- **PyPDF2 3.0.1** - PDF parsing
- **python-docx 1.1.0** - DOCX parsing
- **bcrypt 4.1.2** - Password hashing

## License

MIT License
