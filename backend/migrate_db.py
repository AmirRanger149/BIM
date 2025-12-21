#!/usr/bin/env python3
"""
Migration script to add missing columns to database tables
"""
import sqlite3

def add_missing_columns():
    """Add missing columns to articles and gallery_items tables"""
    try:
        conn = sqlite3.connect('bim.db')
        cursor = conn.cursor()

        # Check and add columns to articles table
        cursor.execute("PRAGMA table_info(articles)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'iframe_url' not in columns:
            cursor.execute("ALTER TABLE articles ADD COLUMN iframe_url VARCHAR(500)")
            print("Added iframe_url to articles")

        if 'model_url' not in columns:
            cursor.execute("ALTER TABLE articles ADD COLUMN model_url VARCHAR(500)")
            print("Added model_url to articles")

        if 'model_type' not in columns:
            cursor.execute("ALTER TABLE articles ADD COLUMN model_type VARCHAR(20) DEFAULT 'auto'")
            print("Added model_type to articles")

        # Check and add columns to gallery_items table
        cursor.execute("PRAGMA table_info(gallery_items)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'iframe_url' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN iframe_url VARCHAR(500)")
            print("Added iframe_url to gallery_items")

        if 'model_url' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN model_url VARCHAR(500)")
            print("Added model_url to gallery_items")

        if 'model_type' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN model_type VARCHAR(20) DEFAULT 'auto'")
            print("Added model_type to gallery_items")

        if 'duration' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN duration VARCHAR(50)")
            print("Added duration to gallery_items")

        if 'views' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN views INTEGER DEFAULT 0")
            print("Added views to gallery_items")

        if 'comments' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN comments INTEGER DEFAULT 0")
            print("Added comments to gallery_items")

        if 'technologies' not in columns:
            cursor.execute("ALTER TABLE gallery_items ADD COLUMN technologies TEXT")
            print("Added technologies to gallery_items")

        conn.commit()
        print("Migration completed successfully")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_missing_columns()