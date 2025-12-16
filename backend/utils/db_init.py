"""
Database initialization and seeding utilities.
Handles table creation, indexes, and development seed data.
"""

from extensions import db
from models import Candidate, JobPosition, MatchResult


def init_database(app):
    """
    Initialize the database by creating all tables and indexes.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create additional indexes for performance optimization
        # Note: Most indexes are already defined in the models
        # This function can be extended to add custom indexes if needed
        
        print("✓ Database tables created successfully")
        print("✓ Indexes created successfully")


def seed_database(app):
    """
    Seed the database with sample data for development and testing.
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        # Check if data already exists
        if JobPosition.query.first() is not None:
            print("⚠ Database already contains data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample job positions
        job1 = JobPosition(
            title='Senior Python Developer',
            description='We are looking for an experienced Python developer to join our backend team. '
                       'The ideal candidate will have strong experience with Flask, Django, and RESTful APIs.',
            required_skills=['Python', 'Flask', 'REST API', 'SQL'],
            preferred_skills=['Docker', 'AWS', 'Redis', 'Celery'],
            min_experience_years=5,
            education_level="Bachelor's"
        )
        
        job2 = JobPosition(
            title='Machine Learning Engineer',
            description='Join our AI team to build cutting-edge machine learning models. '
                       'Experience with NLP and deep learning frameworks required.',
            required_skills=['Python', 'TensorFlow', 'PyTorch', 'Machine Learning', 'NLP'],
            preferred_skills=['spaCy', 'Transformers', 'Kubernetes', 'MLOps'],
            min_experience_years=3,
            education_level="Master's"
        )
        
        job3 = JobPosition(
            title='Frontend Developer',
            description='We need a talented frontend developer to create beautiful and responsive user interfaces. '
                       'Strong React skills are essential.',
            created_by=hr_user.id,
            required_skills=['JavaScript', 'React', 'HTML', 'CSS'],
            preferred_skills=['TypeScript', 'Redux', 'Next.js', 'Tailwind CSS'],
            min_experience_years=2,
            education_level="Bachelor's"
        )
        
        db.session.add(job1)
        db.session.add(job2)
        db.session.add(job3)
        db.session.commit()
        
        print("✓ Created 3 sample job positions")
        
        # Create sample candidates
        candidate1 = Candidate(
            name='John Smith',
            email='john.smith@email.com',
            phone='+1-555-0101',
            status='completed',
            total_experience_years=6
        )
        candidate1.set_education([
            {
                'degree': "Bachelor's in Computer Science",
                'institution': 'MIT',
                'year': 2015
            }
        ])
        candidate1.set_experience([
            {
                'title': 'Senior Python Developer',
                'company': 'Tech Corp',
                'duration': '2018-Present',
                'description': 'Developed RESTful APIs using Flask and Django'
            },
            {
                'title': 'Python Developer',
                'company': 'StartupXYZ',
                'duration': '2015-2018',
                'description': 'Built backend services and database systems'
            }
        ])
        candidate1.set_skills([
            {'name': 'Python', 'category': 'programming_languages', 'score': 95, 'years': 6},
            {'name': 'Flask', 'category': 'frameworks', 'score': 90, 'years': 5},
            {'name': 'Django', 'category': 'frameworks', 'score': 85, 'years': 4},
            {'name': 'PostgreSQL', 'category': 'databases', 'score': 80, 'years': 5},
            {'name': 'Docker', 'category': 'tools', 'score': 75, 'years': 3}
        ])
        candidate1.set_certifications(['AWS Certified Developer'])
        
        candidate2 = Candidate(
            name='Sarah Johnson',
            email='sarah.j@email.com',
            phone='+1-555-0102',
            status='completed',
            total_experience_years=4
        )
        candidate2.set_education([
            {
                'degree': "Master's in Artificial Intelligence",
                'institution': 'Stanford University',
                'year': 2019
            }
        ])
        candidate2.set_experience([
            {
                'title': 'ML Engineer',
                'company': 'AI Solutions Inc',
                'duration': '2019-Present',
                'description': 'Developed NLP models and deployed ML pipelines'
            }
        ])
        candidate2.set_skills([
            {'name': 'Python', 'category': 'programming_languages', 'score': 90, 'years': 4},
            {'name': 'TensorFlow', 'category': 'frameworks', 'score': 88, 'years': 3},
            {'name': 'PyTorch', 'category': 'frameworks', 'score': 85, 'years': 3},
            {'name': 'NLP', 'category': 'soft_skills', 'score': 92, 'years': 4},
            {'name': 'spaCy', 'category': 'frameworks', 'score': 80, 'years': 2}
        ])
        
        candidate3 = Candidate(
            name='Mike Chen',
            email='mike.chen@email.com',
            phone='+1-555-0103',
            status='completed',
            total_experience_years=3
        )
        candidate3.set_education([
            {
                'degree': "Bachelor's in Software Engineering",
                'institution': 'UC Berkeley',
                'year': 2020
            }
        ])
        candidate3.set_experience([
            {
                'title': 'Frontend Developer',
                'company': 'WebDev Co',
                'duration': '2020-Present',
                'description': 'Built responsive web applications using React'
            }
        ])
        candidate3.set_skills([
            {'name': 'JavaScript', 'category': 'programming_languages', 'score': 88, 'years': 3},
            {'name': 'React', 'category': 'frameworks', 'score': 90, 'years': 3},
            {'name': 'TypeScript', 'category': 'programming_languages', 'score': 82, 'years': 2},
            {'name': 'HTML', 'category': 'programming_languages', 'score': 95, 'years': 3},
            {'name': 'CSS', 'category': 'programming_languages', 'score': 90, 'years': 3}
        ])
        
        db.session.add(candidate1)
        db.session.add(candidate2)
        db.session.add(candidate3)
        db.session.commit()
        
        print("✓ Created 3 sample candidates")
        
        # Create sample match results
        match1 = MatchResult(
            candidate_id=candidate1.id,
            job_id=job1.id,
            match_score=88.5,
            skill_match_score=92.0,
            experience_match_score=90.0,
            education_match_score=80.0,
            status='Qualified',
            screening_notes='Excellent match. Strong Python and Flask experience with 6 years total experience.'
        )
        
        match2 = MatchResult(
            candidate_id=candidate2.id,
            job_id=job2.id,
            match_score=91.2,
            skill_match_score=95.0,
            experience_match_score=85.0,
            education_match_score=100.0,
            status='Qualified',
            screening_notes='Perfect match. Master\'s degree and strong ML/NLP background.'
        )
        
        match3 = MatchResult(
            candidate_id=candidate3.id,
            job_id=job3.id,
            match_score=86.0,
            skill_match_score=93.0,
            experience_match_score=80.0,
            education_match_score=80.0,
            status='Qualified',
            screening_notes='Good match. Strong React skills and meets experience requirements.'
        )
        
        match4 = MatchResult(
            candidate_id=candidate1.id,
            job_id=job2.id,
            match_score=62.5,
            skill_match_score=45.0,
            experience_match_score=90.0,
            education_match_score=80.0,
            status='Potentially Qualified',
            screening_notes='Has strong Python experience but lacks ML/NLP specialization.'
        )
        
        db.session.add(match1)
        db.session.add(match2)
        db.session.add(match3)
        db.session.add(match4)
        db.session.commit()
        
        print("✓ Created 4 sample match results")
        print("\n✓ Database seeding completed successfully!")
        print("\nSample credentials:")
        print("  Admin: admin@recruitment.com / admin123")
        print("  HR:    hr@recruitment.com / hr123")


def drop_all_tables(app):
    """
    Drop all database tables. Use with caution!
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
        print("✓ All database tables dropped")


if __name__ == '__main__':
    # This allows running the script directly for database initialization
    from app import create_app
    
    app = create_app()
    
    print("Initializing database...")
    init_database(app)
    
    print("\nSeeding database...")
    seed_database(app)
