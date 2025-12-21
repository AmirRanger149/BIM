#!/usr/bin/env python3
"""
Migration script to add iframe_url support to gallery items.
Adds iframe_url column to gallery_items table.
"""

import sqlite3
import sys
from pathlib import Path

# Database path - matches the config in backend/app/config.py
DB_PATH = Path(__file__).parent / "bim.db"

def migrate():
    """Add iframe_url column to gallery_items table"""
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        print("Please run the backend server first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(gallery_items)")
        columns = [col[1] for col in cursor.fetchall()]
        
        migration_done = False
        
        if 'iframe_url' not in columns:
            print("Adding iframe_url column...")
            cursor.execute("""
                ALTER TABLE gallery_items 
                ADD COLUMN iframe_url VARCHAR(500) DEFAULT NULL
            """)
            migration_done = True
        
        if migration_done:
            conn.commit()
            print("✅ Migration completed successfully!")
            print("   - iframe_url: stores iframe URL for 3D viewer (e.g., https://b1m.ir/project/projects/pasargad/3D/)")
        else:
            print("ℹ️  iframe_url column already exists. No migration needed.")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
