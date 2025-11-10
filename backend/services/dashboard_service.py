"""
Dashboard Service for HR analytics and statistics.
Provides aggregated data for the HR dashboard including candidate statistics,
job position metrics, and match score analytics.
"""

from sqlalchemy import func
from extensions import db
from models.candidate import Candidate
from models.job_position import JobPosition
from models.match_result import MatchResult


class DashboardService:
    """
    Service class for generating dashboard statistics and analytics.
    Implements methods for calculating recruitment metrics and data distributions.
    """
    
    @staticmethod
    def get_statistics():
        """
        Get overall recruitment statistics for the dashboard.
        
        Returns:
            dict: Statistics including:
                - total_candidates: Total number of candidates in the system
                - total_jobs: Total number of active job positions
                - avg_match_score: Average match score across all matches
                - qualified_candidates: Number of candidates marked as 'Qualified'
                - recent_uploads: Number of candidates uploaded in the last 7 days
        
        Requirements: 7.1, 7.5
        """
        try:
            # Total candidates
            total_candidates = Candidate.query.filter_by(status='completed').count()
            
            # Total active jobs
            total_jobs = JobPosition.query.filter_by(is_active=True).count()
            
            # Average match score across all match results
            avg_match_score_result = db.session.query(
                func.avg(MatchResult.match_score)
            ).scalar()
            avg_match_score = round(avg_match_score_result, 2) if avg_match_score_result else 0.0
            
            # Count of qualified candidates (distinct candidates with at least one 'Qualified' match)
            qualified_candidates = db.session.query(
                func.count(func.distinct(MatchResult.candidate_id))
            ).filter(
                MatchResult.status == 'Qualified'
            ).scalar() or 0
            
            # Recent uploads (last 7 days) - using a simple approach
            from datetime import datetime, timedelta
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_uploads = Candidate.query.filter(
                Candidate.created_at >= seven_days_ago
            ).count()
            
            return {
                'total_candidates': total_candidates,
                'total_jobs': total_jobs,
                'avg_match_score': avg_match_score,
                'qualified_candidates': qualified_candidates,
                'recent_uploads': recent_uploads
            }
        
        except Exception as e:
            raise Exception(f"Error calculating statistics: {str(e)}")
    
    @staticmethod
    def get_analytics():
        """
        Get detailed analytics data for visualizations.
        
        Returns:
            dict: Analytics data including:
                - skill_distribution: Count of candidates by skill category
                - experience_distribution: Count of candidates by experience level
                - match_score_distribution: Count of matches by score range
        
        Requirements: 7.1, 7.5
        """
        try:
            # Skill distribution - count candidates by skill categories
            skill_distribution = DashboardService._get_skill_distribution()
            
            # Experience distribution - group candidates by experience ranges
            experience_distribution = DashboardService._get_experience_distribution()
            
            # Match score distribution - group matches by score ranges
            match_score_distribution = DashboardService._get_match_score_distribution()
            
            return {
                'skill_distribution': skill_distribution,
                'experience_distribution': experience_distribution,
                'match_score_distribution': match_score_distribution
            }
        
        except Exception as e:
            raise Exception(f"Error calculating analytics: {str(e)}")
    
    @staticmethod
    def _get_skill_distribution():
        """
        Calculate distribution of skills across all candidates.
        
        Returns:
            dict: Skill names mapped to candidate counts
        """
        skill_counts = {}
        
        # Query all completed candidates
        candidates = Candidate.query.filter_by(status='completed').all()
        
        for candidate in candidates:
            skills = candidate.get_skills()
            if skills:
                for skill in skills:
                    skill_name = skill.get('name', '').strip()
                    if skill_name:
                        skill_counts[skill_name] = skill_counts.get(skill_name, 0) + 1
        
        # Sort by count (descending) and return top 20 skills
        sorted_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        
        return sorted_skills
    
    @staticmethod
    def _get_experience_distribution():
        """
        Calculate distribution of candidates by experience level.
        
        Returns:
            dict: Experience ranges mapped to candidate counts
        """
        experience_ranges = {
            '0-2 years': 0,
            '3-5 years': 0,
            '6-10 years': 0,
            '11-15 years': 0,
            '16+ years': 0
        }
        
        # Query all completed candidates
        candidates = Candidate.query.filter_by(status='completed').all()
        
        for candidate in candidates:
            years = candidate.total_experience_years or 0
            
            if years <= 2:
                experience_ranges['0-2 years'] += 1
            elif years <= 5:
                experience_ranges['3-5 years'] += 1
            elif years <= 10:
                experience_ranges['6-10 years'] += 1
            elif years <= 15:
                experience_ranges['11-15 years'] += 1
            else:
                experience_ranges['16+ years'] += 1
        
        return experience_ranges
    
    @staticmethod
    def _get_match_score_distribution():
        """
        Calculate distribution of match results by score ranges.
        
        Returns:
            dict: Score ranges mapped to match counts
        """
        score_ranges = {
            '0-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0,
            '81-100': 0
        }
        
        # Query all match results
        matches = MatchResult.query.all()
        
        for match in matches:
            score = match.match_score
            
            if score <= 20:
                score_ranges['0-20'] += 1
            elif score <= 40:
                score_ranges['21-40'] += 1
            elif score <= 60:
                score_ranges['41-60'] += 1
            elif score <= 80:
                score_ranges['61-80'] += 1
            else:
                score_ranges['81-100'] += 1
        
        return score_ranges
