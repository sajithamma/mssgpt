import sqlite3
from datetime import datetime
from typing import Optional

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('zappo.db')
    cursor = conn.cursor()

    # Create emails table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def save_email(email: str) -> bool:
    """Save an email to the emails table if not already present."""
    try:
        conn = sqlite3.connect('zappo.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO emails (email) VALUES (?)
        ''', (email,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving email: {e}")
        return False

# Initialize database when module is imported
init_db() 