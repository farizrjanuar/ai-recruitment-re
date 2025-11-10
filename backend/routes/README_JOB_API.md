# Job Position API Documentation

## Overview
The Job Position API provides endpoints for managing job positions in the AI Recruitment System. All endpoints require JWT authentication, and most require HR or Admin role.

## Base URL
```
/api/jobs
```

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### 1. Create Job Position
**POST** `/api/jobs`

**Authorization:** HR or Admin role required

**Request Body:**
```json
{
  "title": "Software Engineer",
  "description": "We are looking for a talented software engineer...",
  "required_skills": ["Python", "Flask", "SQL"],
  "preferred_skills": ["Docker", "AWS"],
  "min_experience_years": 3,
  "education_level": "Bachelor's"
}
```

**Response (201):**
```json
{
  "message": "Job position created successfully",
  "job_id": "uuid-here",
  "job": {
    "id": "uuid-here",
    "title": "Software Engineer",
    "description": "...",
    "required_skills": ["Python", "Flask", "SQL"],
    "preferred_skills": ["Docker", "AWS", "React"],
    "min_experience_years": 3,
    "education_level": "Bachelor's",
    "is_active": true,
    "created_by": "user-uuid",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Features:**
- Automatically extracts additional skills from job description using NLP
- Processes job description to identify key requirements
- Validates required fields

---

### 2. List Job Positions
**GET** `/api/jobs`

**Authorization:** Any authenticated user

**Query Parameters:**
- `include_inactive` (optional): Include inactive jobs (default: false)

**Response (200):**
```json
{
  "jobs": [
    {
      "id": "uuid-here",
      "title": "Software Engineer",
      "description": "...",
      "required_skills": ["Python", "Flask"],
      "preferred_skills": ["Docker"],
      "min_experience_years": 3,
      "education_level": "Bachelor's",
      "is_active": true,
      "created_by": "user-uuid",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1
}
```

---

### 3. Get Job Position Details
**GET** `/api/jobs/<job_id>`

**Authorization:** Any authenticated user

**Response (200):**
```json
{
  "id": "uuid-here",
  "title": "Software Engineer",
  "description": "Full job description...",
  "required_skills": ["Python", "Flask", "SQL"],
  "preferred_skills": ["Docker", "AWS"],
  "min_experience_years": 3,
  "education_level": "Bachelor's",
  "is_active": true,
  "created_by": "user-uuid",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**Error (404):**
```json
{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "Job position with ID <job_id> not found"
  }
}
```

---

### 4. Update Job Position
**PUT** `/api/jobs/<job_id>`

**Authorization:** HR or Admin role required

**Request Body:** (all fields optional)
```json
{
  "title": "Senior Software Engineer",
  "description": "Updated description...",
  "required_skills": ["Python", "Django"],
  "preferred_skills": ["Kubernetes"],
  "min_experience_years": 5,
  "education_level": "Master's",
  "is_active": true
}
```

**Response (200):**
```json
{
  "message": "Job position updated successfully",
  "job": {
    "id": "uuid-here",
    "title": "Senior Software Engineer",
    ...
  }
}
```

---

### 5. Deactivate Job Position
**POST** `/api/jobs/<job_id>/deactivate`

**Authorization:** HR or Admin role required

**Response (200):**
```json
{
  "message": "Job position deactivated successfully"
}
```

**Note:** This is a soft delete. The job position remains in the database but is marked as inactive.

---

### 6. Activate Job Position
**POST** `/api/jobs/<job_id>/activate`

**Authorization:** HR or Admin role required

**Response (200):**
```json
{
  "message": "Job position activated successfully"
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid request data |
| AUTH_TOKEN_INVALID | 401 | Invalid or expired token |
| AUTH_INSUFFICIENT_PERMISSIONS | 403 | User lacks required permissions |
| JOB_NOT_FOUND | 404 | Job position not found |
| INTERNAL_ERROR | 500 | Server error |

---

## Service Layer Features

The `JobService` class provides:

1. **NLP Processing**: Automatically extracts skills and requirements from job descriptions using spaCy
2. **Skill Enhancement**: Adds extracted skills to preferred skills list
3. **CRUD Operations**: Complete create, read, update, delete functionality
4. **Soft Delete**: Jobs are deactivated rather than deleted
5. **Validation**: Ensures required fields are present and valid

---

## Usage Examples

### Create a Job Position
```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Developer",
    "description": "Looking for a Python developer with Flask experience",
    "required_skills": ["Python", "Flask"],
    "min_experience_years": 2
  }'
```

### List All Active Jobs
```bash
curl -X GET http://localhost:5000/api/jobs \
  -H "Authorization: Bearer <token>"
```

### Update a Job
```bash
curl -X PUT http://localhost:5000/api/jobs/<job_id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "min_experience_years": 3,
    "preferred_skills": ["Docker", "Kubernetes"]
  }'
```

### Deactivate a Job
```bash
curl -X POST http://localhost:5000/api/jobs/<job_id>/deactivate \
  -H "Authorization: Bearer <token>"
```

---

## Requirements Satisfied

This implementation satisfies the following requirements from the specification:

- **Requirement 4.1**: Job position creation with title, description, and requirements
- **Requirement 4.2**: Specification of minimum and preferred qualifications
- **Requirement 4.3**: NLP processing of job descriptions to extract key requirements
- **Requirement 4.4**: Job position storage with unique identifiers
- **Requirement 4.5**: Update and deactivation of job positions
- **Requirement 9.3**: JWT token verification for protected endpoints
- **Requirement 9.4**: Role-based access control (HR/Admin)
