# Candidate Management API

This document describes the candidate management API endpoints implemented in task 7.

## Endpoints

### 1. Upload CV

Upload and process a candidate's CV file.

**Endpoint:** `POST /api/candidates/upload`

**Authentication:** Required (JWT Bearer token)

**Request:**
- Content-Type: `multipart/form-data`
- Body: 
  - `cv_file`: File (PDF, DOCX, or TXT, max 5MB)

**Response (Success - 201):**
```json
{
  "candidate_id": "uuid-string",
  "status": "completed",
  "message": "CV uploaded and processed successfully"
}
```

**Response (Error - 400):**
```json
{
  "error": {
    "code": "FILE_TOO_LARGE|FILE_INVALID_FORMAT|FILE_UNREADABLE|PROCESSING_ERROR",
    "message": "Error description"
  }
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/candidates/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "cv_file=@/path/to/resume.pdf"
```

---

### 2. List Candidates

Retrieve a paginated list of candidates with optional filtering.

**Endpoint:** `GET /api/candidates`

**Authentication:** Required (JWT Bearer token)

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `status` (optional): Filter by status (`processing`, `completed`, `failed`)
- `skills` (optional): Comma-separated list of skills to filter by

**Response (Success - 200):**
```json
{
  "candidates": [
    {
      "id": "uuid-string",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "skills": [
        {
          "name": "Python",
          "category": "programming_languages",
          "score": 85.5,
          "years": 5
        }
      ],
      "experience": [...],
      "education": [...],
      "total_experience_years": 5,
      "status": "completed",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "pages": 5,
  "has_next": true,
  "has_prev": false
}
```

**Example using curl:**
```bash
# List all candidates (page 1)
curl -X GET http://localhost:5000/api/candidates \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# List candidates with filters
curl -X GET "http://localhost:5000/api/candidates?page=2&limit=10&status=completed&skills=Python,JavaScript" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Get Candidate Details

Retrieve detailed information about a specific candidate.

**Endpoint:** `GET /api/candidates/<candidate_id>`

**Authentication:** Required (JWT Bearer token)

**Path Parameters:**
- `candidate_id`: UUID of the candidate

**Query Parameters:**
- `include_raw_text` (optional): Include raw CV text (default: false)

**Response (Success - 200):**
```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "education": [
    {
      "degree": "Bachelor of Science",
      "institution": "University Name",
      "year": 2018,
      "level": "Bachelor's"
    }
  ],
  "experience": [
    {
      "title": "Software Engineer",
      "company": "Tech Company",
      "duration": "2018 - 2023",
      "description": "Developed web applications..."
    }
  ],
  "skills": [
    {
      "name": "Python",
      "category": "programming_languages",
      "score": 85.5,
      "years": 5
    }
  ],
  "certifications": [],
  "total_experience_years": 5,
  "status": "completed",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Response (Error - 404):**
```json
{
  "error": {
    "code": "CANDIDATE_NOT_FOUND",
    "message": "Candidate with ID xyz not found"
  }
}
```

**Example using curl:**
```bash
# Get candidate details
curl -X GET http://localhost:5000/api/candidates/CANDIDATE_UUID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get candidate details with raw CV text
curl -X GET "http://localhost:5000/api/candidates/CANDIDATE_UUID?include_raw_text=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| FILE_MISSING | 400 | No file provided in request |
| FILE_TOO_LARGE | 400 | File exceeds 5MB limit |
| FILE_INVALID_FORMAT | 400 | File format not supported (must be PDF, DOCX, or TXT) |
| FILE_UNREADABLE | 400 | Cannot extract text from file |
| PROCESSING_ERROR | 400 | Error during CV processing |
| CANDIDATE_DUPLICATE | 409 | Candidate with this email already exists |
| CANDIDATE_NOT_FOUND | 404 | Candidate ID does not exist |
| VALIDATION_ERROR | 400 | Request parameters validation failed |
| DATABASE_ERROR | 500 | Database operation failed |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## Implementation Details

### CandidateService

The `CandidateService` class orchestrates the complete CV processing workflow:

1. **File Validation**: Validates file size, format, and content
2. **Text Extraction**: Extracts text from PDF, DOCX, or TXT files
3. **CV Parsing**: Extracts structured information (name, email, phone, education, experience)
4. **Skill Analysis**: Analyzes and categorizes skills with proficiency scores
5. **Database Storage**: Creates candidate records with all extracted data

### Processing Flow

```
Upload CV → Validate File → Extract Text → Parse CV → Analyze Skills → Save to DB → Return Response
```

### File Handling

- Uploaded files are temporarily saved with secure filenames
- After successful processing, files are deleted (only extracted data is kept)
- Maximum file size: 5MB
- Supported formats: PDF, DOCX, TXT

### Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Get a token by logging in via the `/api/auth/login` endpoint.
