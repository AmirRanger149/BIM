#!/usr/bin/env python3
"""
Migration script to clean HTML tags from gallery item descriptions
"""
import re
import sqlite3

def clean_html_tags(text):
    """Remove HTML tags from text"""
    if not text:
        return text
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def migrate_gallery_descriptions():
    """Clean HTML tags from all gallery item descriptions"""
    try:
        # Connect to database
        conn = sqlite3.connect('bim.db')
        cursor = conn.cursor()

        # Get all descriptions
        cursor.execute("SELECT id, description FROM gallery_items WHERE description IS NOT NULL")
        rows = cursor.fetchall()

        updated_count = 0
        for row in rows:
            item_id, description = row
            cleaned = clean_html_tags(description)
            if cleaned != description:
                print(f"Cleaning description for item {item_id}: '{description}' -> '{cleaned}'")
                cursor.execute("UPDATE gallery_items SET description = ? WHERE id = ?", (cleaned, item_id))
                updated_count += 1

        # Commit changes
        conn.commit()
        print(f"Successfully cleaned {updated_count} gallery item descriptions")

    except Exception as e:
        print(f"Error during migration: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_gallery_descriptions()