"""
Skill Analyzer Module

This module provides functionality to analyze and extract skills from CV text,
categorize them, and score skill proficiency based on context.
"""

import re
import spacy
from typing import Dict, List, Optional, Tuple


class SkillAnalyzer:
    """
    Analyzes CV text to extract, categorize, and score technical and soft skills.
    Uses NLP (spaCy) and pattern matching for skill identification.
    """
    
    def __init__(self):
        """Initialize the Skill Analyzer with spaCy model and skill taxonomy."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
        
        # Define comprehensive skill taxonomy
        self.skill_categories = {
            'programming_languages': [
                'Python', 'JavaScript', 'Java', 'C++', 'C#', 'C', 'Ruby', 'PHP',
                'Swift', 'Kotlin', 'Go', 'Rust', 'TypeScript', 'Scala', 'R',
                'Perl', 'Objective-C', 'Dart', 'MATLAB', 'Shell', 'Bash',
                'PowerShell', 'VBA', 'SQL', 'PL/SQL', 'T-SQL', 'Groovy', 'Lua',
                'Haskell', 'Elixir', 'Clojure', 'F#', 'Julia', 'Assembly'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue.js', 'Vue', 'Node.js', 'Express.js',
                'Django', 'Flask', 'FastAPI', 'Spring', 'Spring Boot', 'Hibernate',
                '.NET', 'ASP.NET', 'Laravel', 'Symfony', 'Ruby on Rails', 'Rails',
                'jQuery', 'Bootstrap', 'Tailwind CSS', 'Material-UI', 'Next.js',
                'Nuxt.js', 'Gatsby', 'Svelte', 'Ember.js', 'Backbone.js',
                'Redux', 'MobX', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
                'Pandas', 'NumPy', 'Apache Spark', 'Hadoop', 'Kafka', 'RabbitMQ',
                'Selenium', 'Cypress', 'Jest', 'Mocha', 'Pytest', 'JUnit',
                'TestNG', 'Cucumber', 'Playwright'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'SQL Server', 'SQLite',
                'Redis', 'Cassandra', 'DynamoDB', 'Elasticsearch', 'MariaDB',
                'CouchDB', 'Neo4j', 'Firebase', 'Firestore', 'Supabase',
                'InfluxDB', 'TimescaleDB', 'Memcached', 'Amazon RDS', 'Azure SQL',
                'Google Cloud SQL', 'Snowflake', 'BigQuery', 'Redshift'
            ],
            'tools': [
                'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Docker', 'Kubernetes',
                'Jenkins', 'Travis CI', 'CircleCI', 'GitHub Actions', 'GitLab CI',
                'Terraform', 'Ansible', 'Chef', 'Puppet', 'Vagrant', 'AWS',
                'Azure', 'Google Cloud', 'GCP', 'Heroku', 'Netlify', 'Vercel',
                'JIRA', 'Confluence', 'Trello', 'Asana', 'Slack', 'VS Code',
                'Visual Studio', 'IntelliJ IDEA', 'PyCharm', 'Eclipse', 'Postman',
                'Insomnia', 'Swagger', 'Nginx', 'Apache', 'Linux', 'Unix',
                'Windows Server', 'Bash', 'PowerShell', 'Vim', 'Emacs',
                'Webpack', 'Vite', 'Babel', 'ESLint', 'Prettier', 'npm', 'yarn',
                'pip', 'Maven', 'Gradle', 'Make', 'CMake', 'Figma', 'Sketch',
                'Adobe XD', 'Photoshop', 'Illustrator', 'Tableau', 'Power BI',
                'Grafana', 'Prometheus', 'Datadog', 'New Relic', 'Splunk'
            ],
            'soft_skills': [
                'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
                'Critical Thinking', 'Analytical', 'Project Management',
                'Time Management', 'Adaptability', 'Creativity', 'Collaboration',
                'Presentation', 'Negotiation', 'Conflict Resolution',
                'Decision Making', 'Strategic Planning', 'Mentoring', 'Coaching',
                'Agile', 'Scrum', 'Kanban', 'Stakeholder Management',
                'Client Relations', 'Customer Service', 'Public Speaking',
                'Writing', 'Documentation', 'Research', 'Innovation',
                'Attention to Detail', 'Organization', 'Multitasking',
                'Self-motivated', 'Proactive', 'Results-driven'
            ],
            'cloud_platforms': [
                'AWS', 'Amazon Web Services', 'Azure', 'Microsoft Azure',
                'Google Cloud', 'GCP', 'Google Cloud Platform', 'IBM Cloud',
                'Oracle Cloud', 'DigitalOcean', 'Linode', 'Heroku', 'Netlify',
                'Vercel', 'Cloudflare', 'Alibaba Cloud'
            ],
            'methodologies': [
                'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'CI/CD',
                'Test-Driven Development', 'TDD', 'Behavior-Driven Development',
                'BDD', 'Microservices', 'RESTful API', 'GraphQL', 'SOAP',
                'Object-Oriented Programming', 'OOP', 'Functional Programming',
                'Design Patterns', 'MVC', 'MVVM', 'Clean Architecture',
                'Domain-Driven Design', 'DDD'
            ],
            'certifications': [
                'AWS Certified', 'Azure Certified', 'Google Cloud Certified',
                'PMP', 'Scrum Master', 'CSM', 'CISSP', 'CompTIA', 'CCNA',
                'CCNP', 'RHCE', 'RHCSA', 'CKA', 'CKAD', 'Oracle Certified',
                'Microsoft Certified', 'Salesforce Certified'
            ]
        }
        
        # Create a flat list of all skills for quick lookup (lowercase for matching)
        self.all_skills_lower = {}
        for category, skills in self.skill_categories.items():
            for skill in skills:
                self.all_skills_lower[skill.lower()] = {
                    'name': skill,
                    'category': category
                }
        
        # Common skill aliases and variations
        self.skill_aliases = {
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'py': 'Python',
            'k8s': 'Kubernetes',
            'postgres': 'PostgreSQL',
            'mongo': 'MongoDB',
            'react.js': 'React',
            'vue.js': 'Vue',
            'node': 'Node.js',
            'express': 'Express.js',
            'next': 'Next.js',
            'nuxt': 'Nuxt.js',
            'tf': 'TensorFlow',
            'sklearn': 'Scikit-learn',
            'aws': 'AWS',
            'gcp': 'Google Cloud',
            'ci/cd': 'CI/CD',
            'rest': 'RESTful API',
            'oop': 'Object-Oriented Programming',
            'tdd': 'Test-Driven Development',
            'bdd': 'Behavior-Driven Development',
            'ddd': 'Domain-Driven Design'
        }

    def analyze_skills(self, text: str) -> List[Dict[str, any]]:
        """
        Analyze CV text to extract and categorize skills.
        
        Uses both NER (Named Entity Recognition) and pattern matching to identify skills.
        Categorizes skills and calculates proficiency scores based on context.
        
        Args:
            text: CV text to analyze
            
        Returns:
            List of skill dictionaries with keys:
            - name: Skill name
            - category: Skill category
            - score: Proficiency score (0-100)
            - years: Years of experience with the skill (if found)
        """
        skills_found = {}  # Use dict to avoid duplicates (key is lowercase skill name)
        
        # Process text with spaCy
        doc = self.nlp(text.lower())
        
        # Method 1: Pattern matching with skill taxonomy
        for skill_lower, skill_info in self.all_skills_lower.items():
            # Create regex pattern for whole word matching
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            
            if re.search(pattern, text.lower()):
                skill_name = skill_info['name']
                skill_key = skill_name.lower()
                
                if skill_key not in skills_found:
                    # Calculate skill score based on context
                    score = self.calculate_skill_score(skill_name, text)
                    
                    # Extract years of experience for this skill
                    years = self.extract_experience_years(text, skill_name)
                    
                    skills_found[skill_key] = {
                        'name': skill_name,
                        'category': skill_info['category'],
                        'score': score,
                        'years': years
                    }
        
        # Method 2: Check for skill aliases
        for alias, canonical_name in self.skill_aliases.items():
            pattern = r'\b' + re.escape(alias) + r'\b'
            
            if re.search(pattern, text.lower()):
                skill_key = canonical_name.lower()
                
                if skill_key not in skills_found:
                    # Find the category for this skill
                    category = self._get_skill_category(canonical_name)
                    
                    if category:
                        score = self.calculate_skill_score(canonical_name, text)
                        years = self.extract_experience_years(text, canonical_name)
                        
                        skills_found[skill_key] = {
                            'name': canonical_name,
                            'category': category,
                            'score': score,
                            'years': years
                        }
        
        # Convert dict to list and sort by score
        skills_list = list(skills_found.values())
        skills_list.sort(key=lambda x: x['score'], reverse=True)
        
        return skills_list
    
    def calculate_skill_score(self, skill: str, text: str) -> float:
        """
        Calculate proficiency score for a skill based on context analysis.
        
        Scoring factors:
        - Frequency of mention (more mentions = higher score)
        - Context keywords (expert, proficient, advanced, etc.)
        - Years of experience mentioned
        - Position in CV (skills section vs. passing mention)
        
        Args:
            skill: Skill name
            text: Full CV text
            
        Returns:
            Proficiency score (0-100)
        """
        score = 50.0  # Base score
        
        skill_lower = skill.lower()
        text_lower = text.lower()
        
        # Factor 1: Frequency of mention (up to +20 points)
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        mentions = len(re.findall(pattern, text_lower))
        
        if mentions >= 5:
            score += 20
        elif mentions >= 3:
            score += 15
        elif mentions >= 2:
            score += 10
        elif mentions >= 1:
            score += 5
        
        # Factor 2: Proficiency keywords in context (up to +20 points)
        proficiency_keywords = {
            'expert': 20,
            'advanced': 18,
            'proficient': 15,
            'experienced': 12,
            'skilled': 10,
            'strong': 8,
            'solid': 6,
            'familiar': 3,
            'basic': -5,
            'beginner': -10,
            'learning': -5
        }
        
        # Get context around skill mentions (100 chars before and after)
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - 100)
            end = min(len(text_lower), match.end() + 100)
            context = text_lower[start:end]
            
            for keyword, points in proficiency_keywords.items():
                if keyword in context:
                    score += points
                    break  # Only count once per context
        
        # Factor 3: Years of experience (up to +15 points)
        years = self.extract_experience_years(text, skill)
        if years:
            if years >= 5:
                score += 15
            elif years >= 3:
                score += 10
            elif years >= 1:
                score += 5
        
        # Factor 4: Appears in skills section (up to +10 points)
        skills_section = self._extract_skills_section(text_lower)
        if skills_section and skill_lower in skills_section:
            score += 10
        
        # Factor 5: Action verbs indicating active use (up to +10 points)
        action_verbs = [
            'developed', 'built', 'created', 'designed', 'implemented',
            'architected', 'led', 'managed', 'optimized', 'deployed',
            'maintained', 'integrated', 'automated', 'configured'
        ]
        
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - 150)
            end = match.end()
            context = text_lower[start:end]
            
            for verb in action_verbs:
                if verb in context:
                    score += 10
                    break
        
        # Normalize score to 0-100 range
        score = max(0, min(100, score))
        
        return round(score, 1)
    
    def extract_experience_years(self, text: str, skill: str) -> Optional[int]:
        """
        Extract years of experience for a specific skill from CV text.
        
        Looks for patterns like:
        - "5 years of Python experience"
        - "Python (3 years)"
        - "3+ years experience with Python"
        
        Args:
            text: CV text
            skill: Skill name
            
        Returns:
            Years of experience or None if not found
        """
        skill_lower = skill.lower()
        text_lower = text.lower()
        
        # Find all mentions of the skill
        skill_pattern = r'\b' + re.escape(skill_lower) + r'\b'
        
        for match in re.finditer(skill_pattern, text_lower):
            # Get context around the skill (200 chars before and after)
            start = max(0, match.start() - 200)
            end = min(len(text_lower), match.end() + 200)
            context = text_lower[start:end]
            
            # Pattern 1: "X years" or "X+ years"
            years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
            years_matches = re.findall(years_pattern, context)
            
            if years_matches:
                # Return the first (or largest) number found
                years = max(int(y) for y in years_matches)
                return years
            
            # Pattern 2: "(X years)" or "[X years]"
            paren_pattern = r'[\(\[](\d+)\+?\s*(?:years?|yrs?)[\)\]]'
            paren_matches = re.findall(paren_pattern, context)
            
            if paren_matches:
                years = max(int(y) for y in paren_matches)
                return years
        
        return None
    
    def _get_skill_category(self, skill_name: str) -> Optional[str]:
        """
        Get the category for a skill name.
        
        Args:
            skill_name: Skill name
            
        Returns:
            Category name or None
        """
        for category, skills in self.skill_categories.items():
            if skill_name in skills:
                return category
        
        return None
    
    def _is_common_word(self, word: str) -> bool:
        """
        Check if a word is a common English word (not a technical skill).
        
        Args:
            word: Word to check
            
        Returns:
            True if common word
        """
        common_words = {
            'experience', 'work', 'project', 'team', 'company', 'role',
            'position', 'responsibilities', 'skills', 'education', 'university',
            'college', 'degree', 'bachelor', 'master', 'year', 'month',
            'present', 'current', 'description', 'summary', 'objective',
            'profile', 'contact', 'email', 'phone', 'address', 'name',
            'date', 'location', 'city', 'state', 'country', 'website'
        }
        
        return word.lower() in common_words
    
    def _is_technical_context(self, token, doc) -> bool:
        """
        Check if a token appears in a technical context.
        
        Args:
            token: spaCy token
            doc: spaCy doc
            
        Returns:
            True if in technical context
        """
        # Get surrounding tokens (5 before and after)
        token_idx = token.i
        start_idx = max(0, token_idx - 5)
        end_idx = min(len(doc), token_idx + 6)
        
        context_tokens = [t.text.lower() for t in doc[start_idx:end_idx]]
        
        # Technical context indicators
        technical_indicators = [
            'using', 'with', 'including', 'such as', 'like', 'framework',
            'library', 'tool', 'technology', 'platform', 'language',
            'database', 'api', 'development', 'programming', 'software',
            'application', 'system', 'web', 'mobile', 'cloud', 'data'
        ]
        
        for indicator in technical_indicators:
            if indicator in ' '.join(context_tokens):
                return True
        
        return False
    
    def _infer_skill_category(self, skill: str, text: str) -> Optional[str]:
        """
        Infer the category of a skill based on context.
        
        Args:
            skill: Skill name
            text: Full CV text
            
        Returns:
            Inferred category or None
        """
        skill_lower = skill.lower()
        text_lower = text.lower()
        
        # Get context around skill
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - 100)
            end = min(len(text_lower), match.end() + 100)
            context = text_lower[start:end]
            
            # Check for category indicators
            if any(word in context for word in ['programming', 'language', 'code', 'script']):
                return 'programming_languages'
            elif any(word in context for word in ['framework', 'library']):
                return 'frameworks'
            elif any(word in context for word in ['database', 'db', 'sql', 'nosql']):
                return 'databases'
            elif any(word in context for word in ['tool', 'platform', 'software']):
                return 'tools'
            elif any(word in context for word in ['cloud', 'aws', 'azure', 'gcp']):
                return 'cloud_platforms'
            elif any(word in context for word in ['agile', 'scrum', 'methodology', 'approach']):
                return 'methodologies'
        
        # Default to 'tools' if can't determine
        return 'tools'
    
    def _extract_skills_section(self, text: str) -> Optional[str]:
        """
        Extract the skills section from CV text.
        
        Args:
            text: CV text (lowercase)
            
        Returns:
            Skills section text or None
        """
        lines = text.split('\n')
        section_start = -1
        section_end = len(lines)
        
        # Find skills section start
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if any(keyword in line_stripped for keyword in ['skills', 'technical skills', 'competencies', 'expertise']):
                if len(line_stripped) < 50:  # Likely a section header
                    section_start = i
                    break
        
        if section_start == -1:
            return None
        
        # Find section end (next section header)
        common_sections = [
            'experience', 'work', 'employment', 'education', 'projects',
            'certifications', 'awards', 'publications', 'references', 'interests'
        ]
        
        for i in range(section_start + 1, len(lines)):
            line_stripped = lines[i].strip()
            if len(line_stripped) < 50:
                for section in common_sections:
                    if section in line_stripped and line_stripped.index(section) < 5:
                        section_end = i
                        break
            if section_end != len(lines):
                break
        
        # Extract section text
        section_lines = lines[section_start:section_end]
        return '\n'.join(section_lines)
