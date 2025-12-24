"""
CV Parser Service

This service provides functionality to parse CV text and extract structured information
including contact details, education, work experience, and skills.
"""

import re
import spacy
from typing import Dict, List, Optional, Tuple


class CVParserService:
    """
    Service for parsing CV text and extracting structured candidate information.
    Uses NLP (spaCy) and regex patterns for information extraction.
    """
    
    def __init__(self):
        """Initialize the CV Parser with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
    
    def extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract contact information from CV text.
        
        Extracts:
        - Name (using NER and heuristics)
        - Email address
        - Phone number
        
        Args:
            text: Raw CV text
            
        Returns:
            Dictionary with 'name', 'email', and 'phone' keys
        """
        contact_info = {
            'name': None,
            'email': None,
            'phone': None
        }
        
        # Extract email
        contact_info['email'] = self._extract_email(text)
        
        # Extract phone
        contact_info['phone'] = self._extract_phone(text)
        
        # Extract name
        contact_info['name'] = self._extract_name(text)
        
        return contact_info
    
    def _extract_email(self, text: str) -> Optional[str]:
        """
        Extract email address from text using regex.
        
        Args:
            text: Text to search
            
        Returns:
            Email address or None
        """
        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        matches = re.findall(email_pattern, text)
        
        if matches:
            # Return the first email found
            return matches[0].lower()
        
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """
        Extract phone number from text using regex.
        Handles multiple formats:
        - (123) 456-7890
        - 123-456-7890
        - 123.456.7890
        - 1234567890
        - +1 123 456 7890
        
        Args:
            text: Text to search
            
        Returns:
            Phone number or None
        """
        # Phone number patterns (various formats)
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # International and US formats
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890 or 123-456-7890
            r'\d{10}',  # 1234567890
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Clean up the phone number
                phone = matches[0]
                # Remove extra characters but keep digits and +
                phone = re.sub(r'[^\d+]', '', phone)
                return phone
        
        return None
    
    def _extract_name(self, text: str) -> Optional[str]:
        """
        Extract candidate name from CV text.
        
        Strategy:
        1. Check first few lines for all-caps names (common CV format)
        2. Look for PERSON entities using spaCy NER
        3. Use heuristics to identify the most likely name
        4. Try first non-empty line if it looks like a name
        
        Args:
            text: CV text
            
        Returns:
            Candidate name or None
        """
        # Get first 500 characters (name is usually at the top)
        header_text = text[:500]
        lines = text.split('\n')
        
        # Strategy 1: Check first non-empty line if it looks like a simple name (2-4 words, alphabetic)
        for i, line in enumerate(lines[:3]):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if line looks like a simple name (2-4 words, mostly alphabetic)
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if all words are alphabetic (allow dots for middle initials)
                if all(word.replace('.', '').replace(',', '').replace("'", '').isalpha() for word in words):
                    # Check it's not too long
                    if len(line) <= 50:
                        return ' '.join(words)
        
        # Strategy 2: Check first few lines for all-caps names (common CV format)
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if line is mostly uppercase and looks like a name
            words = line.split()
            if len(words) >= 2 and line.isupper():
                # Check if all words are alphabetic (with spaces)
                if all(word.replace('.', '').replace(',', '').isalpha() for word in words):
                    # This is likely a name in all caps
                    return ' '.join(words)
        
        # Strategy 3: Use spaCy NER for PERSON entities
        doc = self.nlp(header_text)
        
        # Extract PERSON entities
        person_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
        if person_entities:
            # Return the first person entity found
            # Clean up the name (remove extra whitespace and common non-name words)
            name = ' '.join(person_entities[0].split())
            # Remove common suffix words that shouldn't be in names
            name_words = name.split()
            filtered_words = [w for w in name_words if w.lower() not in 
                            ['email', 'phone', 'tel', 'fax', 'mobile', 'address', 'cv', 'resume']]
            if len(filtered_words) >= 2:
                return ' '.join(filtered_words)
            elif len(filtered_words) == 1 and len(name_words) == 1:
                return filtered_words[0]
        
        # Strategy 3: Try to find name in first non-empty line with heuristics
        lines = text.split('\n')
        for i, line in enumerate(lines[:10]):  # Check first 10 lines
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip lines that look like section headers or labels
            line_lower = line.lower()
            skip_keywords = ['curriculum', 'vitae', 'resume', 'cv', 'email', 'phone', 
                           'address', 'objective', 'summary', 'professional', 'profile', 
                           'contact', 'personal', 'information']
            if any(keyword in line_lower for keyword in skip_keywords):
                continue
            
            # Name should be reasonably short
            if len(line) > 60:
                continue
            
            # Check if line contains email or phone (skip if it does)
            if '@' in line or re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line):
                continue
            
            # Check if it looks like a name (1-4 words, mostly alphabetic)
            words = line.split()
            if 1 <= len(words) <= 4:
                # Check if words are mostly alphabetic (allow dots and commas for middle initials)
                valid_words = []
                for word in words:
                    clean_word = word.replace('.', '').replace(',', '').replace("'", '')
                    if clean_word and (clean_word.isalpha() or 
                                     (len(clean_word) <= 3 and any(c.isalpha() for c in clean_word))):
                        valid_words.append(word)
                
                # If at least 2 valid words that look like names, use it
                if len(valid_words) >= 2:
                    # Remove common non-name words
                    filtered_words = [w for w in valid_words if w.lower() not in 
                                    ['email', 'phone', 'tel', 'fax', 'mobile', 'address']]
                    if len(filtered_words) >= 2:
                        return ' '.join(filtered_words)
                    elif len(valid_words) >= 2:
                        return ' '.join(valid_words[:2])  # Take first 2 words only
                # If first line and at least 1 valid word, might be single name
                elif i == 0 and len(valid_words) >= 1:
                    return ' '.join(valid_words)
        
        # Fallback 2: Look for "Name:" or "Candidate:" pattern
        name_pattern = r'(?:name|candidate)[\s:]+([A-Z][a-zA-Z\s.]+?)(?:\n|email|phone|$)'
        match = re.search(name_pattern, text[:500], re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if 2 <= len(name.split()) <= 4:
                return name
        
        return None
    
    def extract_education(self, text: str) -> List[Dict[str, Optional[str]]]:
        """
        Extract education information from CV text.
        
        Extracts:
        - Degree/qualification
        - Institution/university
        - Graduation year
        - Education level (Bachelor's, Master's, PhD, etc.)
        
        Args:
            text: CV text
            
        Returns:
            List of education dictionaries
        """
        education_list = []
        
        # Common degree keywords
        degree_patterns = [
            r'\b(Ph\.?D\.?|Doctor of Philosophy|Doctorate)\b',
            r'\b(Master[\'s]*|M\.?S\.?|M\.?A\.?|MBA|M\.?Tech|M\.?Eng)\b',
            r'\b(Bachelor[\'s]*|B\.?S\.?|B\.?A\.?|B\.?Tech|B\.?Eng|Undergraduate)\b',
            r'\b(Associate[\'s]*|A\.?S\.?|A\.?A\.?)\b',
            r'\b(Diploma|Certificate)\b',
        ]
        
        # Education level mapping
        degree_level_map = {
            'phd': 'PhD',
            'doctor': 'PhD',
            'doctorate': 'PhD',
            'master': "Master's",
            'mba': "Master's",
            'bachelor': "Bachelor's",
            'undergraduate': "Bachelor's",
            'associate': "Associate's",
            'diploma': 'Diploma',
            'certificate': 'Certificate'
        }
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Look for education section
        education_section = self._extract_section(text, ['education', 'academic', 'qualification'])
        
        if education_section:
            # Extract years (4-digit numbers that look like years)
            years = re.findall(r'\b(19\d{2}|20\d{2})\b', education_section)
            
            # Extract organizations (likely universities)
            orgs = [ent.text for ent in self.nlp(education_section).ents if ent.label_ == "ORG"]
            
            # Find degree mentions
            for pattern in degree_patterns:
                matches = re.finditer(pattern, education_section, re.IGNORECASE)
                
                for match in matches:
                    degree = match.group(0)
                    match_pos = match.start()
                    
                    # Get context around the degree (200 chars before and after)
                    context_start = max(0, match_pos - 200)
                    context_end = min(len(education_section), match_pos + 200)
                    context = education_section[context_start:context_end]
                    
                    # Find institution in context
                    institution = None
                    
                    # First, try to find university/college patterns
                    university_patterns = [
                        r'(Universitas\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)',  # Universitas Telkom
                        r'(University\s+of\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)',  # University of X
                        r'([A-Z][a-zA-Z]+\s+University)',  # X University
                        r'(Institut\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)',  # Institut Teknologi
                        r'([A-Z][a-zA-Z]+\s+Institute)',  # X Institute
                        r'([A-Z][a-zA-Z]+\s+College)',  # X College
                    ]
                    
                    for uni_pattern in university_patterns:
                        uni_matches = re.findall(uni_pattern, context, re.IGNORECASE)
                        if uni_matches:
                            # Get the first university match and clean it
                            institution = uni_matches[0].strip()
                            # Remove trailing punctuation, line breaks, and extra whitespace
                            institution = re.sub(r'[\n\r]+', ' ', institution)  # Replace newlines with space
                            institution = re.sub(r'\s+', ' ', institution)  # Normalize whitespace
                            institution = re.sub(r'[\s\-–,;.]+$', '', institution)
                            break
                    
                    # If no university pattern found, use ORG entities but filter carefully
                    if not institution:
                        context_orgs = [ent.text for ent in self.nlp(context).ents if ent.label_ == "ORG"]
                        # Filter out obvious non-institution orgs
                        for org in context_orgs:
                            org_lower = org.lower()
                            # Skip if it looks like a degree program name
                            if any(deg in org_lower for deg in ['undergraduate', 'bachelor', 'master', 'phd', 'informatics', 'engineering', 'science', 'student', 'association']):
                                continue
                            # Must have at least 2 words to be a valid institution
                            if len(org.split()) < 2:
                                continue
                            institution = org
                            break
                    
                    # Find year in context
                    year = None
                    context_years = re.findall(r'\b(19\d{2}|20\d{2})\b', context)
                    if context_years:
                        # Take the most recent year
                        year = max(context_years)
                    
                    # Extract field of study/major/program
                    field = None
                    
                    # Strategy 1: Look for field right after degree (e.g., "Undergraduate Informatics", "Bachelor Computer Science")
                    # Get the line containing the degree
                    degree_lines = [line for line in context.split('\n') if degree.lower() in line.lower()]
                    if degree_lines:
                        degree_line = degree_lines[0].strip()
                        # Try to extract field from the same line as degree
                        # Pattern: degree_word followed by potential field name
                        simple_pattern = r'\b' + re.escape(degree) + r'\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\b'
                        simple_match = re.search(simple_pattern, degree_line, re.IGNORECASE)
                        if simple_match:
                            potential_field = simple_match.group(1).strip()
                            # Filter out if it's an institution keyword
                            if not any(word in potential_field.lower() for word in ['university', 'universitas', 'institute', 'institut', 'college', 'school']):
                                field = potential_field
                    
                    # Strategy 2: Look for "in/of" patterns (e.g., "Bachelor of Science in Computer Science")
                    if not field:
                        field_patterns = [
                            r'(?:in|of)\s+([A-Z][a-zA-Z\s]+?)(?:\s*,|\s*\n|\s+at|\s+from|\s+\-)',
                        ]
                        
                        for field_pattern in field_patterns:
                            field_matches = re.findall(field_pattern, context, re.IGNORECASE)
                            if field_matches:
                                field = field_matches[0].strip()
                                # Clean up the field - remove common noise words
                                field = re.sub(r'\b(degree|program|major|concentration|specialization|science)\b', '', field, flags=re.IGNORECASE).strip()
                                # Remove trailing punctuation
                                field = re.sub(r'[\s\-–,;.]+$', '', field)
                                # Only accept if it's not the institution name and has reasonable length
                                if field and len(field) > 2 and len(field) < 50:
                                    break
                                else:
                                    field = None
                            else:
                                field = None
                    
                    # Determine education level
                    education_level = self._determine_education_level(degree, degree_level_map)
                    
                    education_entry = {
                        'degree': degree,
                        'field': field,
                        'institution': institution,
                        'year': int(year) if year else None,
                        'level': education_level
                    }
                    
                    # Avoid duplicates
                    if education_entry not in education_list:
                        education_list.append(education_entry)
        
        return education_list
    
    def _extract_section(self, text: str, keywords: List[str]) -> Optional[str]:
        """
        Extract a section from CV text based on keywords.
        
        Args:
            text: Full CV text
            keywords: List of keywords that might indicate the section
            
        Returns:
            Section text or None
        """
        lines = text.split('\n')
        section_start = -1
        section_end = len(lines)
        
        # Find section start
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            for keyword in keywords:
                if keyword in line_lower and len(line_lower) < 50:
                    section_start = i
                    break
            if section_start != -1:
                break
        
        if section_start == -1:
            return None
        
        # Find section end (next section header or end of document)
        common_sections = [
            'experience', 'work', 'employment', 'skills', 'projects',
            'certifications', 'awards', 'publications', 'references'
        ]
        
        for i in range(section_start + 1, len(lines)):
            line_lower = lines[i].lower().strip()
            # Check if this line is a new section header
            if len(line_lower) < 50:
                for section in common_sections:
                    if section in line_lower and line_lower.index(section) < 5:
                        section_end = i
                        break
            if section_end != len(lines):
                break
        
        # Extract section text
        section_lines = lines[section_start:section_end]
        return '\n'.join(section_lines)
    
    def _determine_education_level(self, degree: str, level_map: Dict[str, str]) -> str:
        """
        Determine education level from degree string.
        
        Args:
            degree: Degree string
            level_map: Mapping of keywords to education levels
            
        Returns:
            Education level string
        """
        degree_lower = degree.lower()
        
        for keyword, level in level_map.items():
            if keyword in degree_lower:
                return level
        
        return 'Other'

    def extract_experience(self, text: str) -> Tuple[List[Dict[str, Optional[str]]], int]:
        """
        Extract work experience information from CV text.
        
        Extracts:
        - Job titles
        - Companies
        - Duration/dates
        - Job descriptions
        - Calculates total years of experience
        
        Args:
            text: CV text
            
        Returns:
            Tuple of (experience list, total years of experience)
        """
        experience_list = []
        
        # Look for experience section
        experience_section = self._extract_section(
            text, 
            ['experience', 'work', 'employment', 'professional', 'career']
        )
        
        if not experience_section:
            return [], 0
        
        # Process with spaCy
        doc = self.nlp(experience_section)
        
        # Extract organizations (companies)
        companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        # Extract date ranges
        date_ranges = self._extract_date_ranges(experience_section)
        
        # Split experience section into entries (by line breaks or bullet points)
        lines = experience_section.split('\n')
        
        current_entry = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line contains a company name
            line_doc = self.nlp(line)
            line_orgs = [ent.text for ent in line_doc.ents if ent.label_ == "ORG"]
            
            # Check if line contains dates
            line_dates = re.findall(r'\b(19\d{2}|20\d{2})\b', line)
            
            # Heuristic: If line has company or dates, it might be a new entry
            if line_orgs or line_dates or self._looks_like_job_title(line):
                # Save previous entry if exists
                if current_entry and current_entry.get('title'):
                    experience_list.append(current_entry)
                
                # Start new entry
                current_entry = {
                    'title': None,
                    'company': None,
                    'duration': None,
                    'description': ''
                }
                
                # Try to extract job title
                if self._looks_like_job_title(line):
                    # Extract title (before company or dates)
                    title = self._extract_job_title(line)
                    current_entry['title'] = title
                
                # Extract company
                if line_orgs:
                    current_entry['company'] = line_orgs[0]
                
                # Extract duration
                if line_dates:
                    duration = self._format_duration(line_dates, line)
                    current_entry['duration'] = duration
            
            elif current_entry:
                # Add to description
                if current_entry['description']:
                    current_entry['description'] += ' ' + line
                else:
                    current_entry['description'] = line
        
        # Add last entry
        if current_entry and current_entry.get('title'):
            experience_list.append(current_entry)
        
        # Calculate total years of experience
        total_years = self._calculate_total_experience(date_ranges)
        
        return experience_list, total_years
    
    def _extract_date_ranges(self, text: str) -> List[Tuple[int, int]]:
        """
        Extract date ranges from text.
        
        Args:
            text: Text to search
            
        Returns:
            List of (start_year, end_year) tuples
        """
        date_ranges = []
        
        # Pattern for date ranges: "2018 - 2020", "2018-2020", "2018 to 2020"
        range_pattern = r'\b(19\d{2}|20\d{2})\s*[-–to]+\s*(19\d{2}|20\d{2}|present|current)\b'
        
        matches = re.finditer(range_pattern, text, re.IGNORECASE)
        
        from datetime import datetime
        current_year = datetime.now().year
        
        for match in matches:
            start_year = int(match.group(1))
            end_year_str = match.group(2).lower()
            
            if end_year_str in ['present', 'current']:
                end_year = current_year
            else:
                end_year = int(end_year_str)
            
            date_ranges.append((start_year, end_year))
        
        return date_ranges
    
    def _looks_like_job_title(self, line: str) -> bool:
        """
        Check if a line looks like a job title.
        
        Args:
            line: Line of text
            
        Returns:
            True if line looks like a job title
        """
        # Job title indicators
        title_keywords = [
            'engineer', 'developer', 'manager', 'analyst', 'designer',
            'consultant', 'specialist', 'coordinator', 'director', 'lead',
            'senior', 'junior', 'intern', 'associate', 'assistant',
            'architect', 'scientist', 'researcher', 'administrator'
        ]
        
        line_lower = line.lower()
        
        # Check if line contains job title keywords
        for keyword in title_keywords:
            if keyword in line_lower:
                return True
        
        return False
    
    def _extract_job_title(self, line: str) -> str:
        """
        Extract job title from a line.
        
        Args:
            line: Line containing job title
            
        Returns:
            Job title string
        """
        # Remove dates and company info
        # Remove patterns like "at Company" or "@ Company"
        title = re.sub(r'\s+(at|@)\s+.*', '', line, flags=re.IGNORECASE)
        
        # Remove date patterns
        title = re.sub(r'\b(19\d{2}|20\d{2})\b.*', '', title)
        title = re.sub(r'\(.*?\)', '', title)  # Remove parentheses
        
        # Clean up
        title = title.strip(' ,-–|')
        
        return title
    
    def _format_duration(self, years: List[str], context: str) -> str:
        """
        Format duration string from years.
        
        Args:
            years: List of year strings
            context: Context text
            
        Returns:
            Formatted duration string
        """
        if len(years) >= 2:
            return f"{years[0]} - {years[-1]}"
        elif len(years) == 1:
            # Check if "present" or "current" is in context
            if re.search(r'\b(present|current)\b', context, re.IGNORECASE):
                return f"{years[0]} - Present"
            return years[0]
        
        return None
    
    def _calculate_total_experience(self, date_ranges: List[Tuple[int, int]]) -> int:
        """
        Calculate total years of experience from date ranges.
        
        Args:
            date_ranges: List of (start_year, end_year) tuples
            
        Returns:
            Total years of experience
        """
        if not date_ranges:
            return 0
        
        # Sort date ranges
        date_ranges = sorted(date_ranges)
        
        # Merge overlapping ranges
        merged_ranges = []
        current_start, current_end = date_ranges[0]
        
        for start, end in date_ranges[1:]:
            if start <= current_end:
                # Overlapping, extend current range
                current_end = max(current_end, end)
            else:
                # Non-overlapping, save current and start new
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        
        # Add last range
        merged_ranges.append((current_start, current_end))
        
        # Calculate total years
        total_years = sum(end - start for start, end in merged_ranges)
        
        return total_years

    def parse_cv(self, text: str) -> Dict:
        """
        Main method to parse CV text and extract all information.
        
        Combines all extraction methods to create a structured Candidate Profile.
        Handles extraction failures gracefully.
        
        Args:
            text: Raw CV text
            
        Returns:
            Dictionary containing structured candidate profile with keys:
            - name, email, phone (contact info)
            - education (list of education entries)
            - experience (list of experience entries)
            - total_experience_years (calculated total)
            - raw_text (original text)
            - extraction_status (success/partial/failed)
            - extraction_errors (list of errors if any)
        """
        profile = {
            'name': None,
            'email': None,
            'phone': None,
            'education': [],
            'experience': [],
            'total_experience_years': 0,
            'raw_text': text,
            'extraction_status': 'success',
            'extraction_errors': []
        }
        
        # Extract contact information
        try:
            contact_info = self.extract_contact_info(text)
            profile['name'] = contact_info.get('name')
            profile['email'] = contact_info.get('email')
            profile['phone'] = contact_info.get('phone')
        except Exception as e:
            profile['extraction_errors'].append(f"Contact info extraction failed: {str(e)}")
            profile['extraction_status'] = 'partial'
        
        # Extract education
        try:
            education = self.extract_education(text)
            profile['education'] = education
        except Exception as e:
            profile['extraction_errors'].append(f"Education extraction failed: {str(e)}")
            profile['extraction_status'] = 'partial'
        
        # Extract experience
        try:
            experience, total_years = self.extract_experience(text)
            profile['experience'] = experience
            profile['total_experience_years'] = total_years
        except Exception as e:
            profile['extraction_errors'].append(f"Experience extraction failed: {str(e)}")
            profile['extraction_status'] = 'partial'
        
        # Check if critical information is missing
        if not profile['name'] and not profile['email']:
            profile['extraction_status'] = 'failed'
            profile['extraction_errors'].append("Critical information missing: name and email")
        
        # If all extractions failed, mark as failed
        if len(profile['extraction_errors']) >= 3:
            profile['extraction_status'] = 'failed'
        
        return profile
