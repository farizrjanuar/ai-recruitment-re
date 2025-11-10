# Matching API Documentation

## Overview

The Matching API provides endpoints for calculating and retrieving candidate-job matching scores. It uses machine learning algorithms to analyze compatibility between candidates and job positions based on skills, experience, and education.

## Endpoints

### 1. Calculate Matches for Candidate

Calculate match scores for a candidate against all active job positions.

**Endpoint:** `POST /api/matching/calculate/:candidate_id`

**Authentication:** Required (JWT)

**Parameters:**
- `candidate_id` (path): ID of the candidate

**Response (200 OK):**
```json
{
  "candidate_id": "uuid",
  "matches": [
    {
      "id": "uuid",
      "candidate_id": "uuid",
      "job_id": "uuid",
      "job_title": "Senior Software Engineer",
      "job_description": "...",
      "match_score": 85.5,
      "breakdown": {
        "skill_match": 90.0,
        "experience_match": 85.0,
        "education_match": 80.0
      },
      "status": "Qualified",
      "screening_notes": "Candidate meets the job requirements...",
      "calculated_at": "2025-11-10T12:00:00"
    }
  ],
  "total_matches": 5
}
```

**Error Responses:**
- `400`: Candidate profile incomplete
- `404`: Candidate not found
- `401`: Unauthorized

---

### 2. Get Candidates for Job

Get ranked list of candidates for a specific job position with optional filtering.

**Endpoint:** `GET /api/matching/job/:job_id`

**Authentication:** Required (JWT)

**Parameters:**
- `job_id` (path): ID of the job position

**Query Parameters:**
- `min_score` (optional): Minimum match score threshold (0-100)
- `status` (optional): Filter by qualification status
  - Values: `Qualified`, `Potentially Qualified`, `Not Qualified`, `all`
  - Default: `all`
- `limit` (optional): Maximum number of results to return

**Response (200 OK):**
```json
{
  "job_id": "uuid",
  "job_title": "Senior Software Engineer",
  "candidates": [
    {
      "id": "uuid",
      "candidate_id": "uuid",
      "candidate_name": "John Doe",
      "candidate_email": "john@example.com",
      "candidate_phone": "+1234567890",
      "candidate_experience_years": 8,
      "candidate_skills": [
        {"name": "Python", "category": "programming_languages", "score": 95.0}
      ],
      "job_id": "uuid",
      "match_score": 85.5,
      "breakdown": {
        "skill_match": 90.0,
        "experience_match": 85.0,
        "education_match": 80.0
      },
      "status": "Qualified",
      "screening_notes": "...",
      "calculated_at": "2025-11-10T12:00:00"
    }
  ],
  "total_candidates": 10,
  "filters": {
    "min_score": 70.0,
    "status": "Qualified",
    "limit": null
  }
}
```

**Error Responses:**
- `400`: Invalid query parameters
- `404`: Job position not found
- `401`: Unauthorized

---

### 3. Get Matches for Candidate

Get all match results for a specific candidate.

**Endpoint:** `GET /api/matching/candidate/:candidate_id`

**Authentication:** Required (JWT)

**Parameters:**
- `candidate_id` (path): ID of the candidate

**Query Parameters:**
- `min_score` (optional): Minimum match score threshold (0-100)

**Response (200 OK):**
```json
{
  "candidate_id": "uuid",
  "candidate_name": "John Doe",
  "matches": [
    {
      "id": "uuid",
      "candidate_id": "uuid",
      "job_id": "uuid",
      "job_title": "Senior Software Engineer",
      "job_description": "...",
      "job_is_active": true,
      "match_score": 85.5,
      "breakdown": {
        "skill_match": 90.0,
        "experience_match": 85.0,
        "education_match": 80.0
      },
      "status": "Qualified",
      "screening_notes": "...",
      "calculated_at": "2025-11-10T12:00:00"
    }
  ],
  "total_matches": 5,
  "filters": {
    "min_score": null
  }
}
```

**Error Responses:**
- `400`: Invalid query parameters
- `404`: Candidate not found
- `401`: Unauthorized

---

### 4. Calculate Single Match

Calculate match score for a specific candidate-job pair.

**Endpoint:** `POST /api/matching/single/:candidate_id/:job_id`

**Authentication:** Required (JWT)

**Parameters:**
- `candidate_id` (path): ID of the candidate
- `job_id` (path): ID of the job position

**Response (200 OK):**
```json
{
  "match": {
    "id": "uuid",
    "candidate_id": "uuid",
    "job_id": "uuid",
    "job_title": "Senior Software Engineer",
    "job_description": "...",
    "match_score": 85.5,
    "breakdown": {
      "skill_match": 90.0,
      "experience_match": 85.0,
      "education_match": 80.0
    },
    "status": "Qualified",
    "screening_notes": "...",
    "calculated_at": "2025-11-10T12:00:00"
  }
}
```

**Error Responses:**
- `400`: Candidate profile incomplete
- `404`: Candidate or job not found
- `401`: Unauthorized

---

## Matching Algorithm

The matching system uses a weighted scoring approach:

### Score Components

1. **Skill Match (50% weight)**
   - Uses TF-IDF vectorization and cosine similarity
   - Exact match bonuses for required skills (5 points each, up to 50 points)
   - Exact match bonuses for preferred skills (2 points each, up to 20 points)
   - Semantic similarity score (up to 30 points)

2. **Experience Match (30% weight)**
   - Compares candidate's years of experience with job requirement
   - 100 points if meets or exceeds requirement
   - 80-99 points if has 80%+ of required experience
   - Proportional scoring below 80%

3. **Education Match (20% weight)**
   - Compares education levels using hierarchy
   - 100 points if meets or exceeds requirement
   - 70 points if one level below
   - 40 points if two levels below

### Qualification Status

Candidates are categorized as:

- **Qualified**: Overall score ≥ 70% AND skill score ≥ 60%
- **Potentially Qualified**: Overall score ≥ 50% OR (score ≥ 40% AND skill score ≥ 50%)
- **Not Qualified**: Below the above thresholds

### Screening Notes

The system generates detailed screening notes explaining:
- Strengths (high scores in various areas)
- Considerations (moderate scores)
- Gaps (areas where candidate falls short)
- Required skills coverage
- Experience and education analysis

---

## Usage Examples

### Calculate matches for a candidate

```bash
curl -X POST http://localhost:5000/api/matching/calculate/candidate-uuid \
  -H "Authorization: Bearer <jwt-token>"
```

### Get top qualified candidates for a job

```bash
curl -X GET "http://localhost:5000/api/matching/job/job-uuid?status=Qualified&min_score=70" \
  -H "Authorization: Bearer <jwt-token>"
```

### Get all matches for a candidate

```bash
curl -X GET "http://localhost:5000/api/matching/candidate/candidate-uuid?min_score=50" \
  -H "Authorization: Bearer <jwt-token>"
```

### Calculate specific candidate-job match

```bash
curl -X POST http://localhost:5000/api/matching/single/candidate-uuid/job-uuid \
  -H "Authorization: Bearer <jwt-token>"
```

---

## Integration Notes

1. **Automatic Matching**: After a candidate's CV is processed (status = 'completed'), you can trigger matching calculation
2. **Match Updates**: Calling calculate endpoints will update existing match results if they already exist
3. **Performance**: Match calculations are performed synchronously and typically complete in < 2 seconds
4. **Database Storage**: All match results are stored in the database for quick retrieval
5. **Filtering**: Use query parameters to filter results by score and qualification status

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| CANDIDATE_NOT_FOUND | 404 | Candidate ID does not exist |
| JOB_NOT_FOUND | 404 | Job position ID does not exist |
| VALIDATION_ERROR | 400 | Invalid request parameters or incomplete data |
| PROCESSING_ERROR | 500 | Error during match calculation |
| AUTH_TOKEN_MISSING | 401 | No JWT token provided |
| AUTH_TOKEN_INVALID | 401 | Invalid JWT token |
| AUTH_TOKEN_EXPIRED | 401 | JWT token has expired |
