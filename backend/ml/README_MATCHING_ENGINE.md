# Matching Engine Documentation

## Overview

The `MatchingEngine` class calculates compatibility scores between candidates and job positions using machine learning techniques including TF-IDF vectorization and cosine similarity.

## Features

### 1. Skill Matching (50% weight)
- Uses TF-IDF vectorization and cosine similarity for semantic matching
- Provides bonus scoring for exact matches on required skills
- Differentiates between required and preferred skills
- Returns score from 0-100

### 2. Experience Matching (30% weight)
- Compares candidate's years of experience with job requirements
- Full score (100) for meeting or exceeding requirements
- Proportional scoring for partial matches
- Returns score from 0-100

### 3. Education Matching (20% weight)
- Uses education level hierarchy (High School → PhD)
- Compares candidate's highest education with job requirements
- Partial credit for being close to required level
- Returns score from 0-100

### 4. Candidate Screening
- Categorizes candidates as "Qualified", "Potentially Qualified", or "Not Qualified"
- Generates detailed screening notes explaining the decision
- Identifies strengths, considerations, and gaps

## Usage Example

```python
from ml.matching_engine import MatchingEngine

# Initialize engine
engine = MatchingEngine()

# Prepare candidate data
candidate = {
    'skills': [
        {'name': 'Python', 'category': 'programming_languages', 'score': 85, 'years': 3},
        {'name': 'Flask', 'category': 'frameworks', 'score': 75, 'years': 2}
    ],
    'total_experience_years': 3,
    'education': [
        {'degree': "Bachelor's in Computer Science", 'institution': 'University', 'year': 2020}
    ]
}

# Prepare job data
job = {
    'required_skills': ['Python', 'Flask', 'PostgreSQL'],
    'preferred_skills': ['Docker', 'AWS'],
    'min_experience_years': 2,
    'education_level': "Bachelor's"
}

# Calculate match scores
match_scores = engine.calculate_match_score(candidate, job)
# Returns: {
#     'match_score': 75.5,
#     'skill_match_score': 65.0,
#     'experience_match_score': 100.0,
#     'education_match_score': 100.0
# }

# Screen candidate
status, notes = engine.screen_candidate(candidate, job, match_scores)
# Returns: ("Qualified", "Detailed screening notes...")
```

## Scoring Algorithm

### Overall Match Score
```
Overall Score = (Skill Score × 0.5) + (Experience Score × 0.3) + (Education Score × 0.2)
```

### Skill Matching Details
- **Exact Match Component (70%)**: 
  - Required skills: 5 points per match (up to 50 points)
  - Preferred skills: 2 points per match (up to 20 points)
- **Semantic Similarity (30%)**: 
  - TF-IDF vectorization + cosine similarity (up to 30 points)

### Experience Matching Details
- 100% if candidate meets/exceeds requirement
- 80-99% if candidate has 80%+ of required experience
- Proportional scoring below 80%

### Education Matching Details
- 100% if meets or exceeds requirement
- 70% if one level below
- 40% if two levels below
- 20% if more than two levels below

## Qualification Thresholds

- **Qualified**: Overall score ≥ 70% AND skill score ≥ 60%
- **Potentially Qualified**: Overall score ≥ 50% OR (score ≥ 40% AND skill score ≥ 50%)
- **Not Qualified**: Below thresholds

## Education Level Hierarchy

1. High School
2. Diploma
3. Associate
4. Bachelor's
5. Master's / MBA
6. PhD / Doctorate

## Dependencies

- `scikit-learn`: TF-IDF vectorization and cosine similarity
- `numpy`: Numerical operations

## Notes

- The engine is stateless and can be reused for multiple calculations
- All scores are rounded to 2 decimal places
- Empty or missing data is handled gracefully with default scores
