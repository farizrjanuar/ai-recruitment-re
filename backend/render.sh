build:
  - pip install -r requirements.txt
  - python -m spacy download en_core_web_sm

start: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
