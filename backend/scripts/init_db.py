#!/usr/bin/env python3
"""
Database initialization script for MzeeChakula backend.
Creates all tables defined in SQLAlchemy models.

Usage:
    python scripts/init_db.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.models.database import Base, engine, SQLALCHEMY_DATABASE_URL
from api.models.user import UserDB
from api.models.chat import ConversationDB, MessageDB

def init_database():
    """Initialize database by creating all tables."""
    print(f"Initializing database at: {SQLALCHEMY_DATABASE_URL}")
    print("Creating tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Successfully created all tables:")
        print("  - users")
        print("  - conversations")
        print("  - messages")
        print("\nDatabase initialization complete!")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def drop_all_tables():
    """Drop all tables (use with caution!)."""
    print(f"WARNING: This will drop all tables in: {SQLALCHEMY_DATABASE_URL}")
    confirm = input("Are you sure? Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        try:
            Base.metadata.drop_all(bind=engine)
            print("✓ Successfully dropped all tables")
            return True
        except Exception as e:
            print(f"✗ Error dropping tables: {e}")
            return False
    else:
        print("Operation cancelled")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (DANGEROUS!)"
    )
    
    args = parser.parse_args()
    
    if args.drop:
        if drop_all_tables():
            init_database()
    else:
        init_database()
