"""
Matching Engine Module

This module provides functionality to calculate compatibility scores between
candidates and job positions using machine learning techniques.
"""

from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class MatchingEngine:
    """
    Calculates compatibility scores between candidates and job positions.
    
    Uses TF-IDF vectorization and cosine similarity for skill matching,
    combined with experience and education level comparisons to produce
    an overall match score with detailed breakdown.
    """
    
    def __init__(self):
        """Initialize the Matching Engine with TF-IDF vectorizer."""
        # Initialize TF-IDF vectorizer with appropriate parameters
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Limit to top 500 features
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=1,  # Minimum document frequency
            max_df=0.95  # Maximum document frequency (ignore very common terms)
        )
        
        # Education level hierarchy for comparison
        self.education_levels = {
            'high school': 1,
            'diploma': 2,
            'associate': 3,
            'bachelor': 4,
            "bachelor's": 4,
            'master': 5,
            "master's": 5,
            'mba': 5,
            'phd': 6,
            'doctorate': 6
        }
    
    def _prepare_skill_text(self, skills: List[str]) -> str:
        """
        Convert a list of skills into a single text string for vectorization.
        
        Args:
            skills: List of skill names
            
        Returns:
            str: Space-separated skill text
        """
        if not skills:
            return ""
        
        # Join skills with spaces, lowercase for consistency
        return " ".join(str(skill).lower() for skill in skills)
    
    def _normalize_education_level(self, education_level: Optional[str]) -> int:
        """
        Convert education level string to numeric value for comparison.
        
        Args:
            education_level: Education level string (e.g., "Bachelor's", "Master's")
            
        Returns:
            int: Numeric education level (1-6), or 0 if not found
        """
        if not education_level:
            return 0
        
        education_lower = education_level.lower()
        
        # Check for exact matches or partial matches
        for level_name, level_value in self.education_levels.items():
            if level_name in education_lower:
                return level_value
        
        # Default to 0 if not recognized
        return 0

    def _calculate_skill_match(
        self, 
        candidate_skills: List[Dict], 
        required_skills: List[str], 
        preferred_skills: List[str]
    ) -> float:
        """
        Calculate skill match score between candidate and job requirements.
        
        Uses TF-IDF vectorization and cosine similarity to compare skills,
        with bonus scoring for exact matches on required skills.
        
        Args:
            candidate_skills: List of candidate skill dicts with 'name' key
            required_skills: List of required skill names for the job
            preferred_skills: List of preferred skill names for the job
            
        Returns:
            float: Skill match score (0-100)
        """
        if not candidate_skills:
            return 0.0
        
        # Extract skill names from candidate skills
        candidate_skill_names = [
            skill['name'].lower() if isinstance(skill, dict) else str(skill).lower()
            for skill in candidate_skills
        ]
        
        # Normalize job skills
        required_skills_lower = [str(s).lower() for s in (required_skills or [])]
        preferred_skills_lower = [str(s).lower() for s in (preferred_skills or [])]
        
        # If no job skills specified, return base score
        if not required_skills_lower and not preferred_skills_lower:
            return 50.0
        
        # Calculate exact match bonuses
        exact_match_score = 0.0
        
        # Required skills: 5 points per match (up to 50 points)
        if required_skills_lower:
            required_matches = sum(
                1 for req_skill in required_skills_lower 
                if any(req_skill in cand_skill or cand_skill in req_skill 
                       for cand_skill in candidate_skill_names)
            )
            required_match_rate = required_matches / len(required_skills_lower)
            exact_match_score += required_match_rate * 50
        
        # Preferred skills: 2 points per match (up to 20 points)
        if preferred_skills_lower:
            preferred_matches = sum(
                1 for pref_skill in preferred_skills_lower 
                if any(pref_skill in cand_skill or cand_skill in pref_skill 
                       for cand_skill in candidate_skill_names)
            )
            preferred_match_rate = preferred_matches / len(preferred_skills_lower)
            exact_match_score += preferred_match_rate * 20
        
        # Calculate semantic similarity using TF-IDF and cosine similarity
        semantic_score = 0.0
        
        try:
            # Prepare text for vectorization
            candidate_text = self._prepare_skill_text(candidate_skill_names)
            job_skills_combined = required_skills_lower + preferred_skills_lower
            job_text = self._prepare_skill_text(job_skills_combined)
            
            if candidate_text and job_text:
                # Fit and transform both texts
                tfidf_matrix = self.vectorizer.fit_transform([candidate_text, job_text])
                
                # Calculate cosine similarity
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                # Convert similarity (0-1) to score (0-30)
                semantic_score = similarity * 30
        except Exception:
            # If TF-IDF fails (e.g., empty vocabulary), use only exact matches
            semantic_score = 0.0
        
        # Combine exact match score (70% weight) and semantic score (30% weight)
        total_score = exact_match_score + semantic_score
        
        # Normalize to 0-100 range
        total_score = max(0.0, min(100.0, total_score))
        
        return round(total_score, 2)

    def _calculate_experience_match(
        self, 
        candidate_experience_years: int, 
        required_experience_years: int
    ) -> float:
        """
        Calculate experience match score by comparing years of experience.
        
        Scoring formula:
        - If candidate meets or exceeds requirement: 100 points
        - If candidate has 80%+ of required experience: 80-99 points
        - If candidate has less: proportional score
        
        Args:
            candidate_experience_years: Candidate's total years of experience
            required_experience_years: Job's minimum required years
            
        Returns:
            float: Experience match score (0-100)
        """
        # If no experience required, everyone gets full score
        if not required_experience_years or required_experience_years == 0:
            return 100.0
        
        # If candidate has no experience
        if not candidate_experience_years or candidate_experience_years == 0:
            return 0.0
        
        # Calculate ratio
        experience_ratio = candidate_experience_years / required_experience_years
        
        # If candidate meets or exceeds requirement
        if experience_ratio >= 1.0:
            return 100.0
        
        # If candidate has 80%+ of required experience, give high score
        if experience_ratio >= 0.8:
            # Scale from 80 to 99 based on ratio (0.8 to 1.0)
            score = 80 + (experience_ratio - 0.8) * 95
            return round(min(100.0, score), 2)
        
        # For less than 80%, use proportional scoring
        # 0% experience = 0 points, 80% experience = 80 points
        score = experience_ratio * 100
        
        return round(max(0.0, score), 2)
    
    def _calculate_education_match(
        self, 
        candidate_education: List[Dict], 
        required_education_level: Optional[str]
    ) -> float:
        """
        Calculate education match score by comparing education levels.
        
        Uses education level hierarchy to determine if candidate meets
        or exceeds the required education level.
        
        Args:
            candidate_education: List of candidate education dicts with 'degree' key
            required_education_level: Required education level string
            
        Returns:
            float: Education match score (0-100)
        """
        # If no education required, everyone gets full score
        if not required_education_level:
            return 100.0
        
        # If candidate has no education data
        if not candidate_education:
            return 0.0
        
        # Get required education level value
        required_level = self._normalize_education_level(required_education_level)
        
        # If required level not recognized, give base score
        if required_level == 0:
            return 50.0
        
        # Find candidate's highest education level
        candidate_max_level = 0
        
        for edu in candidate_education:
            if isinstance(edu, dict) and 'degree' in edu:
                degree = edu['degree']
                level = self._normalize_education_level(degree)
                candidate_max_level = max(candidate_max_level, level)
        
        # If candidate has no recognized education
        if candidate_max_level == 0:
            return 20.0  # Give some base score for having education data
        
        # Calculate score based on level comparison
        if candidate_max_level >= required_level:
            # Meets or exceeds requirement
            return 100.0
        elif candidate_max_level == required_level - 1:
            # One level below (e.g., Bachelor's when Master's required)
            return 70.0
        elif candidate_max_level == required_level - 2:
            # Two levels below
            return 40.0
        else:
            # More than two levels below
            return 20.0

    def calculate_match_score(
        self, 
        candidate: Dict, 
        job: Dict
    ) -> Dict[str, float]:
        """
        Calculate overall match score between a candidate and job position.
        
        Combines skill matching (50% weight), experience matching (30% weight),
        and education matching (20% weight) into an overall score with detailed breakdown.
        
        Args:
            candidate: Candidate dictionary with keys:
                - skills: List of skill dicts
                - total_experience_years: Integer
                - education: List of education dicts
            job: Job position dictionary with keys:
                - required_skills: List of skill names
                - preferred_skills: List of skill names
                - min_experience_years: Integer
                - education_level: String
                
        Returns:
            dict: Match result with keys:
                - match_score: Overall score (0-100)
                - skill_match_score: Skills component score
                - experience_match_score: Experience component score
                - education_match_score: Education component score
        """
        # Extract candidate data
        candidate_skills = candidate.get('skills', [])
        candidate_experience = candidate.get('total_experience_years', 0)
        candidate_education = candidate.get('education', [])
        
        # Extract job requirements
        required_skills = job.get('required_skills', [])
        preferred_skills = job.get('preferred_skills', [])
        min_experience = job.get('min_experience_years', 0)
        education_level = job.get('education_level')
        
        # Calculate individual component scores
        skill_score = self._calculate_skill_match(
            candidate_skills, 
            required_skills, 
            preferred_skills
        )
        
        experience_score = self._calculate_experience_match(
            candidate_experience, 
            min_experience
        )
        
        education_score = self._calculate_education_match(
            candidate_education, 
            education_level
        )
        
        # Calculate weighted average
        # Skill: 50%, Experience: 30%, Education: 20%
        overall_score = (
            skill_score * 0.5 +
            experience_score * 0.3 +
            education_score * 0.2
        )
        
        # Round to 2 decimal places
        overall_score = round(overall_score, 2)
        
        return {
            'match_score': overall_score,
            'skill_match_score': skill_score,
            'experience_match_score': experience_score,
            'education_match_score': education_score
        }

    def screen_candidate(
        self, 
        candidate: Dict, 
        job: Dict, 
        match_scores: Dict[str, float]
    ) -> Tuple[str, str]:
        """
        Screen candidate and determine qualification status with reasoning.
        
        Applies minimum criteria to categorize candidates as:
        - "Qualified": Meets all minimum requirements
        - "Potentially Qualified": Close to requirements, worth reviewing
        - "Not Qualified": Does not meet minimum requirements
        
        Args:
            candidate: Candidate dictionary
            job: Job position dictionary
            match_scores: Dictionary with match score breakdown
                
        Returns:
            tuple: (status, screening_notes)
                - status: "Qualified", "Potentially Qualified", or "Not Qualified"
                - screening_notes: Explanation of the screening decision
        """
        overall_score = match_scores['match_score']
        skill_score = match_scores['skill_match_score']
        experience_score = match_scores['experience_match_score']
        education_score = match_scores['education_match_score']
        
        # Extract data for detailed analysis
        candidate_skills = candidate.get('skills', [])
        candidate_experience = candidate.get('total_experience_years', 0)
        required_skills = job.get('required_skills', [])
        min_experience = job.get('min_experience_years', 0)
        education_level = job.get('education_level')
        
        # Build screening notes
        notes = []
        issues = []
        strengths = []
        
        # Analyze skill match
        if skill_score >= 70:
            strengths.append(f"Strong skill match ({skill_score:.1f}%)")
        elif skill_score >= 50:
            notes.append(f"Moderate skill match ({skill_score:.1f}%)")
        else:
            issues.append(f"Low skill match ({skill_score:.1f}%)")
        
        # Check required skills coverage
        if required_skills:
            candidate_skill_names = [
                skill['name'].lower() if isinstance(skill, dict) else str(skill).lower()
                for skill in candidate_skills
            ]
            required_skills_lower = [str(s).lower() for s in required_skills]
            
            matched_required = sum(
                1 for req_skill in required_skills_lower 
                if any(req_skill in cand_skill or cand_skill in req_skill 
                       for cand_skill in candidate_skill_names)
            )
            
            if matched_required == len(required_skills):
                strengths.append("Has all required skills")
            elif matched_required >= len(required_skills) * 0.7:
                notes.append(f"Has {matched_required}/{len(required_skills)} required skills")
            else:
                issues.append(f"Missing key skills ({matched_required}/{len(required_skills)} required skills)")
        
        # Analyze experience match
        if min_experience > 0:
            if experience_score >= 100:
                strengths.append(f"Meets experience requirement ({candidate_experience}+ years)")
            elif experience_score >= 80:
                notes.append(f"Close to experience requirement ({candidate_experience}/{min_experience} years)")
            else:
                issues.append(f"Below experience requirement ({candidate_experience}/{min_experience} years required)")
        
        # Analyze education match
        if education_level:
            if education_score >= 100:
                strengths.append("Meets education requirement")
            elif education_score >= 70:
                notes.append("Education level close to requirement")
            else:
                issues.append("Does not meet education requirement")
        
        # Determine qualification status based on overall score and critical factors
        status = None
        
        # Qualified: High overall score and meets most requirements
        if overall_score >= 70 and skill_score >= 60:
            status = "Qualified"
            summary = "Candidate meets the job requirements and is recommended for interview."
        
        # Potentially Qualified: Moderate score or missing some requirements
        elif overall_score >= 50 or (overall_score >= 40 and skill_score >= 50):
            status = "Potentially Qualified"
            summary = "Candidate shows potential but may need further evaluation."
        
        # Not Qualified: Low score or critical gaps
        else:
            status = "Not Qualified"
            summary = "Candidate does not meet minimum requirements for this position."
        
        # Build final screening notes
        screening_notes = summary
        
        if strengths:
            screening_notes += "\n\nStrengths:\n- " + "\n- ".join(strengths)
        
        if notes:
            screening_notes += "\n\nConsiderations:\n- " + "\n- ".join(notes)
        
        if issues:
            screening_notes += "\n\nGaps:\n- " + "\n- ".join(issues)
        
        screening_notes += f"\n\nOverall Match Score: {overall_score:.1f}%"
        
        return status, screening_notes
