import sys
sys.path.insert(0, '/Users/farizrjanuar/Comproj/ai-recruitment-re/backend')

from services.cv_parser_service import CVParserService
import json

# Test CV text
cv_text = """RINA SUSANTI
Email: rina.susanti@email.com
Phone: +62-812-3456-7890

EDUCATION
Undergraduate Informatics
Universitas Telkom
Graduated: 2026

Bachelor of Science in Computer Science
Massachusetts Institute of Technology
Graduated: 2020

Master of Business Administration
Harvard Business School
Graduated: 2022

EXPERIENCE
Junior Software Developer
PT Tech Indonesia | 2022 - Present
- Developed web applications using React and Python

SKILLS
Programming: Python, JavaScript, Java
"""

parser = CVParserService()
result = parser.parse_cv(cv_text)

print("Parsed Education:")
print(json.dumps(result['education'], indent=2))
