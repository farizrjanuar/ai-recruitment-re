# Implementation Plan - AI Recruitment System

## Overview

This implementation plan breaks down the AI Recruitment System into incremental, actionable coding tasks. Each task builds upon previous work and focuses on delivering functional components that can be tested and integrated progressively.

## Task List

- [x] 1. Set up backend project structure and dependencies
  - Create Flask project directory structure (models/, services/, ml/, routes/, utils/)
  - Create requirements.txt with all necessary dependencies (Flask, SQLAlchemy, spaCy, scikit-learn, PyPDF2, python-docx, Flask-JWT-Extended, Flask-CORS)
  - Create config.py for environment configuration management
  - Create app.py as Flask application entry point with basic setup
  - _Requirements: 10.1, 10.2_

- [x] 2. Implement database models and schema
  - [x] 2.1 Create User model with authentication fields
    - Write User model class with id, email, password_hash, role, timestamps
    - Implement password hashing methods using bcrypt
    - Add SQLAlchemy relationships and constraints
    - _Requirements: 9.2, 9.4_
  
  - [x] 2.2 Create Candidate model with JSON fields
    - Write Candidate model with all fields (name, email, phone, education, experience, skills, etc.)
    - Implement JSON field serialization/deserialization methods
    - Add status enum for processing states
    - _Requirements: 2.4, 10.2_
  
  - [x] 2.3 Create JobPosition model
    - Write JobPosition model with title, description, required_skills, preferred_skills
    - Add foreign key relationship to User (created_by)
    - Implement is_active flag for soft deletion
    - _Requirements: 4.1, 4.4_
  
  - [x] 2.4 Create MatchResult model with scoring fields
    - Write MatchResult model with candidate_id, job_id, match scores
    - Add foreign key relationships to Candidate and JobPosition
    - Implement status enum for qualification levels
    - _Requirements: 5.3, 5.5_
  
  - [x] 2.5 Create database initialization script
    - Write database initialization function with table creation
    - Add database indexes for performance optimization
    - Create seed data function for development/testing
    - _Requirements: 10.3, 10.4_

- [x] 3. Implement authentication system
  - [x] 3.1 Create authentication routes and JWT setup
    - Write /api/auth/register endpoint with validation
    - Write /api/auth/login endpoint with JWT token generation
    - Write /api/auth/refresh endpoint for token renewal
    - Configure Flask-JWT-Extended with secret keys and expiration
    - _Requirements: 9.1, 9.3_
  
  - [x] 3.2 Implement authentication middleware and decorators
    - Create JWT verification decorator for protected routes
    - Implement role-based access control decorator (admin_required, hr_required)
    - Add error handlers for authentication failures
    - _Requirements: 9.3, 9.4, 9.5_
  
  - [ ]* 3.3 Write authentication unit tests
    - Test user registration with valid and invalid data
    - Test login with correct and incorrect credentials
    - Test JWT token generation and verification
    - Test role-based access control
    - _Requirements: 9.1, 9.2, 9.3_

- [x] 4. Implement CV text extraction (ML component)
  - [x] 4.1 Create TextExtractor class for multi-format parsing
    - Write extract_from_pdf method using PyPDF2
    - Write extract_from_docx method using python-docx
    - Write extract_from_txt method for plain text files
    - Implement clean_text method for text normalization
    - Add error handling for corrupted or unreadable files
    - _Requirements: 1.2, 1.5_
  
  - [x] 4.2 Create file validation utilities
    - Write file size validator (max 5MB)
    - Write file format validator (PDF, DOCX, TXT only)
    - Write file content validator (minimum text length)
    - Implement secure filename generation
    - _Requirements: 1.1, 1.3_
  
  - [ ]* 4.3 Write text extraction unit tests
    - Test PDF extraction with sample files
    - Test DOCX extraction with sample files
    - Test error handling for invalid files
    - Test text cleaning and normalization
    - _Requirements: 1.2, 1.5_

- [x] 5. Implement CV parsing and information extraction









  - [x] 5.1 Download and setup spaCy model


    - Install spaCy en_core_web_sm model using python -m spacy download en_core_web_sm


    - Verify model is loaded correctly in the application
    - _Requirements: 2.1, 2.2_
  
  - [x] 5.2 Create CVParserService with contact info extraction


    - Create backend/services/cv_parser_service.py file
    - Write extract_contact_info method using regex patterns for email, phone, name
    - Extract name, email, phone number from CV text
    - Handle multiple formats and edge cases
    - _Requirements: 2.1, 2.5_
  
  - [x] 5.3 Implement education extraction


    - Write extract_education method using NLP and pattern matching
    - Extract degree, institution, graduation year
    - Parse education level (Bachelor's, Master's, PhD, etc.)
    - _Requirements: 2.1_
  
  - [x] 5.4 Implement work experience extraction


    - Write extract_experience method using spaCy NER
    - Extract job titles, companies, duration, descriptions
    - Calculate total years of experience
    - _Requirements: 2.2_
  
  - [x] 5.5 Integrate all extraction methods in parse_cv


    - Combine all extraction methods into main parse_cv function
    - Create structured Candidate Profile JSON
    - Handle extraction failures gracefully
    - _Requirements: 2.4, 2.5_
  
  - [ ]* 5.6 Write CV parsing unit tests
    - Test contact info extraction with various CV formats
    - Test education and experience extraction accuracy
    - Test complete parse_cv workflow
    - _Requirements: 2.1, 2.2, 2.4_

- [x] 6. Implement skill analysis (ML component)




  - [x] 6.1 Create skill taxonomy and SkillAnalyzer class


    - Create backend/ml/skill_analyzer.py file
    - Define skill categories dictionary (programming_languages, frameworks, databases, tools, soft_skills)
    - Load spaCy en_core_web_sm model in __init__
    - Create comprehensive skill keyword lists for pattern matching
    - _Requirements: 3.2_
  
  - [x] 6.2 Implement skill extraction and scoring methods


    - Write analyze_skills method using NER and pattern matching
    - Implement skill categorization logic
    - Write calculate_skill_score method based on context analysis
    - Write extract_experience_years method for skill-specific experience
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ]* 6.3 Write skill analysis unit tests
    - Test skill extraction from sample CV texts
    - Test skill categorization accuracy
    - Test skill scoring algorithm
    - _Requirements: 3.1, 3.2, 3.3_

- [x] 7. Implement candidate management API




  - [x] 7.1 Create CandidateService for business logic


    - Create backend/services/candidate_service.py file
    - Implement process_cv function that orchestrates text extraction, parsing, and skill analysis
    - Write create_candidate method to save candidate data
    - Write get_candidate and list_candidates methods
    - Handle errors and update candidate status accordingly
    - _Requirements: 2.4, 3.5_
  
  - [x] 7.2 Create candidate API routes


    - Create backend/routes/candidate_routes.py file
    - Write POST /api/candidates/upload endpoint with multipart/form-data handling
    - Add file validation and secure storage using FileValidator
    - Trigger CV processing workflow (synchronous for MVP)
    - Return candidate_id and processing status
    - _Requirements: 1.1, 1.4_
  
  - [x] 7.3 Create candidate retrieval endpoints


    - Write GET /api/candidates endpoint with pagination and filtering
    - Write GET /api/candidates/:id endpoint for detailed candidate view
    - Implement query filters (status, skills)
    - Add JWT authentication to all endpoints
    - Register candidate_bp blueprint in app.py
    - _Requirements: 7.2, 7.3_
  
  - [ ]* 7.4 Write candidate API integration tests
    - Test CV upload with valid files
    - Test CV upload with invalid files (size, format)
    - Test candidate retrieval and filtering
    - _Requirements: 1.1, 1.3, 7.2_

- [x] 8. Implement job position management API



  - [x] 8.1 Create JobService for business logic


    - Create backend/services/job_service.py file
    - Implement create_job, get_job, list_jobs, update_job, deactivate_job methods
    - Write process_job_description function using spaCy to extract key requirements
    - Store processed data in JobPosition model
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 8.2 Create job position API routes


    - Create backend/routes/job_routes.py file
    - Write POST /api/jobs endpoint for job creation
    - Write GET /api/jobs endpoint for listing all jobs
    - Write GET /api/jobs/:id endpoint for job details
    - Write PUT /api/jobs/:id endpoint for job updates
    - Add JWT authentication and authorization checks (HR/Admin only)
    - Register job_bp blueprint in app.py
    - _Requirements: 4.1, 4.2, 4.4, 4.5_
  
  - [ ]* 8.3 Write job management API tests
    - Test job creation with valid data
    - Test job retrieval and updates
    - Test authorization for job management
    - _Requirements: 4.1, 4.2, 4.4_

- [x] 9. Implement matching engine (ML component)





  - [x] 9.1 Create MatchingEngine class with TF-IDF vectorizer


    - Create backend/ml/matching_engine.py file
    - Initialize TfidfVectorizer with appropriate parameters
    - Create helper methods for vector conversion
    - _Requirements: 5.2_
  
  - [x] 9.2 Implement skill matching algorithm


    - Write _calculate_skill_match method using cosine similarity
    - Implement TF-IDF vectorization for candidate and job skills
    - Add bonus scoring for exact matches on required skills
    - Weight required vs preferred skills appropriately
    - _Requirements: 5.2, 5.5_
  
  - [x] 9.3 Implement experience and education matching


    - Write _calculate_experience_match method comparing years
    - Write _calculate_education_match method with level mapping
    - Implement scoring formulas for each component
    - _Requirements: 5.2, 5.5_
  
  - [x] 9.4 Implement overall match score calculation


    - Write calculate_match_score method combining all components
    - Apply weighted average (skill 50%, experience 30%, education 20%)
    - Return detailed breakdown of scores
    - _Requirements: 5.3, 5.5_
  
  - [x] 9.5 Implement candidate screening logic


    - Write screen_candidate method applying minimum criteria
    - Categorize as "Qualified", "Potentially Qualified", or "Not Qualified"
    - Generate screening notes explaining the decision
    - _Requirements: 6.2, 6.3, 6.4_
  
  - [ ]* 9.6 Write matching engine unit tests
    - Test skill matching with sample data
    - Test experience and education matching
    - Test overall score calculation accuracy
    - Test screening logic with various scenarios
    - _Requirements: 5.2, 5.3, 6.2_
-

- [x] 10. Implement matching API endpoints



  - [x] 10.1 Create MatchingService for business logic


    - Create backend/services/matching_service.py file
    - Implement calculate_matches method for all active jobs
    - Implement calculate_single_match method for specific candidate-job pair
    - Implement get_candidates_for_job method with ranking
    - Use MatchingEngine to calculate scores and store in MatchResult model
    - _Requirements: 5.1, 5.3, 5.4_
  
  - [x] 10.2 Create matching API routes


    - Create backend/routes/matching_routes.py file
    - Write POST /api/matching/calculate/:candidate_id endpoint
    - Write GET /api/matching/job/:job_id endpoint with ranking
    - Implement filtering by minimum score and qualification status
    - Add JWT authentication to all endpoints
    - Register matching_bp blueprint in app.py
    - _Requirements: 5.1, 5.4, 6.1_
  
  - [ ]* 10.3 Write matching API integration tests
    - Test match calculation for candidate-job pairs
    - Test candidate ranking for jobs
    - Test filtering and sorting functionality
    - _Requirements: 5.1, 5.4, 6.1_

- [x] 11. Implement HR dashboard API




  - [x] 11.1 Create DashboardService for analytics


    - Create backend/services/dashboard_service.py file
    - Implement get_statistics method (total candidates, jobs, avg match scores, qualified candidates)
    - Implement get_analytics method (skill distribution, experience distribution, match score distribution)
    - _Requirements: 7.1, 7.5_
  
  - [x] 11.2 Create dashboard API routes


    - Create backend/routes/dashboard_routes.py file
    - Write GET /api/dashboard/stats endpoint
    - Write GET /api/dashboard/analytics endpoint
    - Add JWT authentication to all endpoints
    - Register dashboard_bp blueprint in app.py
    - _Requirements: 7.1, 7.5_
  
  - [ ]* 11.3 Write dashboard API tests
    - Test statistics calculation accuracy
    - Test analytics data generation
    - _Requirements: 7.1, 7.5_

- [x] 12. Enhance React frontend for backend integration



  - [x] 12.1 Install frontend dependencies


    - Install axios for HTTP requests
    - Install react-router-dom for routing
    - Install chart.js and react-chartjs-2 for data visualization
    - Update package.json with all required dependencies
    - _Requirements: 8.1_
  
  - [x] 12.2 Set up Axios and API configuration


    - Create src/services/api.js with axios instance and base URL configuration
    - Create src/services/authAPI.js for authentication endpoints
    - Create src/services/candidateAPI.js for candidate endpoints
    - Create src/services/jobAPI.js for job endpoints
    - Create src/services/dashboardAPI.js for dashboard endpoints
    - Implement JWT token storage in localStorage
    - Add request interceptor for automatic JWT header injection
    - Add response interceptor for error handling
    - _Requirements: 8.1, 8.2_
  
  - [x] 12.3 Create authentication context and pages


    - Create src/context/AuthContext.js for global auth state
    - Create src/components/Login.js component
    - Create src/components/Register.js component
    - Create src/components/ProtectedRoute.js wrapper component
    - Implement login, register, logout functionality
    - _Requirements: 9.1_
  
  - [x] 12.4 Create CV upload page


    - Create src/pages/UploadCV.js component
    - Implement file upload with drag-and-drop support
    - Add file validation (size, format) on client side
    - Show upload progress and processing status
    - Display success/error messages
    - _Requirements: 1.1, 1.3_
  

  - [x] 12.5 Create candidate list and detail pages

    - Create src/pages/CandidateList.js with pagination
    - Implement filtering by status
    - Create src/pages/CandidateDetail.js showing full profile
    - Display extracted skills, experience, education
    - Show match scores for all positions
    - _Requirements: 7.2, 7.3, 7.4_
  

  - [x] 12.6 Create job management pages

    - Create src/pages/JobList.js showing all positions
    - Create src/pages/JobForm.js for creating/editing jobs
    - Create src/pages/JobDetail.js with candidate matches
    - Add job activation/deactivation toggle
    - _Requirements: 4.1, 4.2, 4.4_
  

  - [x] 12.7 Create HR dashboard page

    - Create src/pages/Dashboard.js with statistics cards
    - Implement charts for skill distribution using Chart.js
    - Show experience level distribution chart
    - Display match score distribution chart
    - Add recent candidates list
    - _Requirements: 7.1, 7.5_
  


  - [x] 12.8 Implement navigation and routing

    - Set up React Router in src/App.js with all routes
    - Create src/components/Navbar.js with role-based menu items
    - Create src/components/NotFound.js for 404 page
    - Update src/App.js to use routing and authentication
    - _Requirements: 8.1_


- [x] 13. Create deployment configuration





  - [x] 13.1 Set up backend for Render/Railway deployment


    - Create Procfile or render.yaml for deployment
    - Add gunicorn to requirements.txt
    - Configure Gunicorn as production WSGI server
    - Update backend/.env.example with all required environment variables
    - Ensure health check endpoint exists in app.py
    - _Requirements: 10.5_
  
  - [x] 13.2 Configure frontend for Vercel deployment


    - Create vercel.json configuration file
    - Create .env.example for frontend with REACT_APP_API_URL
    - Configure build settings in package.json
    - Add deployment documentation to README
    - _Requirements: 8.1_
  
  - [x] 13.3 Create deployment documentation


    - Write step-by-step deployment guide for backend (Render/Railway)
    - Write deployment guide for frontend (Vercel)
    - Document environment variable setup for both
    - Add troubleshooting section

    - _Requirements: 10.1_
- [-] 14. Integration testing and bug fixes


- [ ] 14. Integration testing and bug fixes



  - [ ] 14.1 Test complete CV upload to matching workflow
    - Upload sample CVs through frontend
    - Verify data extraction accuracy
    - Check match score calculations
    - Test dashboard data updates
    - _Requirements: 1.1, 2.1, 5.1, 7.1_
  
  - [ ] 14.2 Test job creation and candidate matching workflow
    - Create job positions through frontend
    - Verify candidate matching results
    - Test filtering and sorting
    - Check authorization and permissions
    - _Requirements: 4.1, 5.1, 6.1_
  
  - [ ] 14.3 Fix identified bugs and edge cases
    - Address any issues found during integration testing
    - Improve error messages and user feedback
    - Optimize performance bottlenecks

    - _Requirements: All_


- [ ] 15. Create project documentation

  - [ ] 15.1 Update README with complete setup instructions
    - Document project overview and features
    - Write local development setup guide for both backend and frontend
    - Document API endpoints
    - Add screenshots and usage examples
    - _Requirements: All_
  
  - [ ] 15.2 Create API documentation
    - Document all API endpoints with request/response examples
    - Add authentication flow documentation
    - Document error codes and messages
    - Create API.md file in backend directory
    - _Requirements: 8.1, 8.3_

## Notes

- Tasks marked with `*` are optional testing tasks that can be skipped for faster MVP delivery
- Each task should be completed and tested before moving to the next
- The implementation follows a bottom-up approach: database → services → ML → API → frontend
- Focus on core functionality first, optimization can be done later
- Use SQLite for local development, PostgreSQL for production deployment
- CORS is already configured in backend/extensions.py and app.py - no additional CORS setup needed
- Global error handlers are already implemented in app.py - focus on custom exception classes if needed
- spaCy model (en_core_web_sm) needs to be downloaded before running CV parsing: `python -m spacy download en_core_web_sm`
