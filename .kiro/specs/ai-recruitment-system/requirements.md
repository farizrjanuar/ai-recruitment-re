# Requirements Document

## Introduction

The AI Recruitment System is a web-based platform designed to automate and optimize the candidate screening and job matching process. The system leverages artificial intelligence and machine learning to analyze candidate CVs, extract relevant information, assess skills and qualifications, and match candidates with suitable job positions. The platform consists of a Python/Flask backend with integrated AI/ML models and a React frontend for user interaction.

## Glossary

- **System**: The AI Recruitment System web application
- **CV Parser**: The component responsible for extracting structured data from uploaded CV files
- **ML Engine**: The machine learning component that performs candidate scoring and job matching
- **Candidate Profile**: A structured digital representation of a candidate's qualifications, skills, and experience
- **Match Score**: A numerical value (0-100) indicating the compatibility between a candidate and a job position
- **HR User**: A human resources professional or recruiter using the system
- **Candidate**: A job applicant who uploads their CV to the system
- **Job Position**: A specific role or vacancy with defined requirements and qualifications
- **API**: The RESTful backend interface that handles communication between frontend and backend
- **Dashboard**: The HR user interface displaying candidate analytics and recruitment metrics

## Requirements

### Requirement 1: CV Upload and Processing

**User Story:** As a Candidate, I want to upload my CV in various formats, so that the system can analyze my qualifications for job positions

#### Acceptance Criteria

1. WHEN a Candidate uploads a file, THE System SHALL accept CV files in PDF, DOCX, and TXT formats with a maximum size of 5MB
2. WHEN a CV file is uploaded, THE CV Parser SHALL extract text content from the file within 10 seconds
3. IF a file exceeds the size limit or has an unsupported format, THEN THE System SHALL return an error message indicating the specific validation failure
4. WHEN text extraction is complete, THE System SHALL store the raw CV text in the database with a unique identifier
5. THE System SHALL validate that uploaded files contain readable text content before processing

### Requirement 2: Candidate Information Extraction

**User Story:** As an HR User, I want the system to automatically extract key information from CVs, so that I can quickly review candidate qualifications without manual data entry

#### Acceptance Criteria

1. WHEN a CV is processed, THE CV Parser SHALL extract the candidate's name, email, phone number, and education details
2. WHEN a CV is processed, THE CV Parser SHALL identify and extract work experience entries including job titles, companies, and duration
3. WHEN a CV is processed, THE CV Parser SHALL extract technical skills, certifications, and languages mentioned in the CV
4. WHEN extraction is complete, THE System SHALL create a Candidate Profile with all extracted information structured in JSON format
5. IF critical information (name or email) cannot be extracted, THEN THE System SHALL flag the profile as incomplete and notify the HR User

### Requirement 3: Skill Analysis and Scoring

**User Story:** As an HR User, I want the system to analyze and score candidate skills, so that I can objectively assess their qualifications

#### Acceptance Criteria

1. WHEN a Candidate Profile is created, THE ML Engine SHALL analyze technical skills using NLP techniques (TF-IDF or Word2Vec)
2. WHEN analyzing skills, THE ML Engine SHALL categorize skills into predefined categories (programming languages, frameworks, tools, soft skills)
3. WHEN skill analysis is complete, THE ML Engine SHALL assign a proficiency score (0-100) for each identified skill based on context and frequency
4. THE ML Engine SHALL identify years of experience for each skill when mentioned in the CV
5. WHEN scoring is complete, THE System SHALL store skill scores in the Candidate Profile

### Requirement 4: Job Position Management

**User Story:** As an HR User, I want to create and manage job positions with specific requirements, so that the system can match candidates accurately

#### Acceptance Criteria

1. WHEN an HR User creates a job position, THE System SHALL accept job title, description, required skills, experience level, and education requirements
2. THE System SHALL allow HR Users to specify minimum and preferred qualifications for each job position
3. WHEN a job position is saved, THE ML Engine SHALL process the job description using NLP to extract key requirements
4. THE System SHALL store job positions with unique identifiers in the database
5. THE System SHALL allow HR Users to update or deactivate existing job positions

### Requirement 5: Candidate-Job Matching

**User Story:** As an HR User, I want the system to automatically match candidates with suitable job positions, so that I can identify the best candidates efficiently

#### Acceptance Criteria

1. WHEN a Candidate Profile is complete, THE ML Engine SHALL calculate Match Scores for all active Job Positions
2. WHEN calculating Match Scores, THE ML Engine SHALL compare candidate skills, experience, and education against job requirements using cosine similarity or neural network models
3. THE ML Engine SHALL generate Match Scores between 0 and 100, where 100 indicates perfect alignment
4. WHEN matching is complete, THE System SHALL rank candidates for each Job Position by Match Score in descending order
5. THE System SHALL provide a breakdown of matching factors (skills match, experience match, education match) for each candidate-job pair

### Requirement 6: Automated Candidate Screening

**User Story:** As an HR User, I want the system to automatically screen candidates based on minimum criteria, so that I only review qualified applicants

#### Acceptance Criteria

1. WHEN a Job Position has minimum requirements defined, THE System SHALL filter candidates who do not meet these requirements
2. THE System SHALL screen candidates based on minimum education level, years of experience, and required skills
3. WHEN screening is complete, THE System SHALL categorize candidates as "Qualified", "Potentially Qualified", or "Not Qualified"
4. IF a candidate is marked "Not Qualified", THEN THE System SHALL provide specific reasons for the rejection
5. THE System SHALL allow HR Users to adjust screening thresholds for each Job Position

### Requirement 7: HR Dashboard and Analytics

**User Story:** As an HR User, I want to view comprehensive recruitment analytics and candidate information, so that I can make informed hiring decisions

#### Acceptance Criteria

1. WHEN an HR User accesses the Dashboard, THE System SHALL display total candidates, active job positions, and average Match Scores
2. THE Dashboard SHALL display a list of candidates for each Job Position sorted by Match Score
3. WHEN viewing a candidate, THE Dashboard SHALL show the complete Candidate Profile, extracted skills, and Match Scores for all positions
4. THE Dashboard SHALL provide filtering options by job position, Match Score range, and qualification status
5. THE Dashboard SHALL display visual charts showing candidate distribution by skills, experience level, and Match Score ranges

### Requirement 8: RESTful API for Frontend Integration

**User Story:** As a Frontend Developer, I want a well-documented RESTful API, so that I can integrate the React frontend with the backend services

#### Acceptance Criteria

1. THE API SHALL provide endpoints for CV upload, candidate retrieval, job position management, and matching results
2. WHEN the API receives a request, THE System SHALL validate authentication tokens using JWT
3. THE API SHALL return responses in JSON format with appropriate HTTP status codes (200, 201, 400, 401, 404, 500)
4. WHEN an error occurs, THE API SHALL return error messages with clear descriptions and error codes
5. THE API SHALL implement CORS (Cross-Origin Resource Sharing) to allow requests from the React frontend

### Requirement 9: User Authentication and Authorization

**User Story:** As an HR User, I want secure login functionality, so that only authorized personnel can access candidate data

#### Acceptance Criteria

1. WHEN an HR User logs in with valid credentials, THE System SHALL generate a JWT token valid for 24 hours
2. THE System SHALL hash and store user passwords using bcrypt with a minimum of 10 salt rounds
3. WHEN accessing protected endpoints, THE API SHALL verify the JWT token and reject requests with invalid or expired tokens
4. THE System SHALL support role-based access control with "Admin" and "HR" roles
5. WHERE an Admin role is assigned, THE System SHALL allow user management operations (create, update, delete users)

### Requirement 10: Data Persistence and Management

**User Story:** As a System Administrator, I want reliable data storage, so that candidate and job information is preserved and retrievable

#### Acceptance Criteria

1. THE System SHALL use PostgreSQL or MongoDB as the primary database for storing all application data
2. WHEN a Candidate Profile is created, THE System SHALL store it with a unique identifier, timestamp, and status
3. THE System SHALL maintain referential integrity between candidates, job positions, and match results
4. THE System SHALL implement database indexes on frequently queried fields (candidate email, job position ID, Match Score)
5. THE System SHALL perform automated database backups daily at 2:00 AM server time
