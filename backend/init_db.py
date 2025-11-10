#!/usr/bin/env python
"""
Database initialization script.
Run this script to create tables and optionally seed with sample data.

Usage:
    python init_db.py              # Initialize tables only
    python init_db.py --seed       # Initialize and seed with sample data
    python init_db.py --reset      # Drop all tables and reinitialize
"""

import sys
from app import create_app
from utils.db_init import init_database, seed_database, drop_all_tables


def main():
    """Main function to handle database initialization."""
    app = create_app()
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--reset' in args:
        print("⚠ WARNING: This will drop all existing tables!")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            drop_all_tables(app)
            init_database(app)
            print("\n✓ Database reset complete")
        else:
            print("Operation cancelled")
            return
    
    if '--seed' in args or '--reset' in args:
        init_database(app)
        seed_database(app)
    else:
        init_database(app)
    
    print("\n✓ Database initialization complete!")


if __name__ == '__main__':
    main()
