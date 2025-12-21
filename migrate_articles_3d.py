#!/usr/bin/env python3
"""
Migration script to add 3D model and iframe support to articles.
Adds iframe_url, model_url, and model_type columns to articles table.
"""

import sqlite3
import sys
from pathlib import Path

# Database path - matches the config in backend/app/config.py
DB_PATH = Path(__file__).parent / "bim.db"

def migrate():
    """Add 3D model columns to articles table"""
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        print("Please run the backend server first to create the database.")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(articles)")
        columns = [col[1] for col in cursor.fetchall()]
        
        migration_done = False
        
        if 'iframe_url' not in columns:
            print("Adding iframe_url column to articles...")
            cursor.execute("""
                ALTER TABLE articles 
                ADD COLUMN iframe_url VARCHAR(500) DEFAULT NULL
            """)
            migration_done = True
        
        if 'model_url' not in columns:
            print("Adding model_url column to articles...")
            cursor.execute("""
                ALTER TABLE articles 
                ADD COLUMN model_url VARCHAR(500) DEFAULT NULL
            """)
            migration_done = True
        
        if 'model_type' not in columns:
            print("Adding model_type column to articles...")
            cursor.execute("""
                ALTER TABLE articles 
                ADD COLUMN model_type VARCHAR(20) DEFAULT 'auto'
            """)
            migration_done = True
        
        if migration_done:
            conn.commit()
            print("✅ Migration completed successfully!")
            print("   - iframe_url: stores iframe URL for 3D viewer")
            print("   - model_url: stores URL to 3D model file (GLTF, GLB, OBJ)")
            print("   - model_type: stores model format (gltf, glb, obj, auto)")
        else:
            print("ℹ️  3D columns already exist in articles table. No migration needed.")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
