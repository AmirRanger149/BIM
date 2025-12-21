#!/usr/bin/env python3
"""
Database migration script to create Settings table
Run this before starting the application
"""

import sys
import os
from sqlalchemy import inspect

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import engine, Base
from app.models import Settings

def create_tables():
    """Create all tables that don't exist"""
    # Create Settings table
    Settings.__table__.create(engine, checkfirst=True)
    print("✅ Settings table created successfully")

if __name__ == "__main__":
    try:
        create_tables()
        print("✅ Database migration completed!")
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        sys.exit(1)
