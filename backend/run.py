#!/usr/bin/env python
"""
Simple runner script for Flask application.
Run with: python run.py
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=False)
