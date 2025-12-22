import sys
sys.path.insert(0, '/Users/farizrjanuar/Comproj/ai-recruitment-re/backend')

from services.cv_parser_service import CVParserService

with open('/Users/farizrjanuar/Comproj/ai-recruitment-re/backend/test_samples/sample_cv_1.txt', 'r') as f:
    cv_text = f.read()

parser = CVParserService()
result = parser.parse_cv(cv_text)

print(f"Extracted Name: '{result['name']}'")
print(f"Expected: 'John Doe'")
print(f"Match: {result['name'] == 'John Doe'}")
