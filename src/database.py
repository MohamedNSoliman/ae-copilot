"""
Database module for user authentication and saved briefs.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

DB_PATH = Path("data/account_briefs.db")


def get_db_connection():
    """Create database connection and ensure tables exist."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    create_tables(conn)
    return conn


def create_tables(conn: sqlite3.Connection):
    """Create database tables if they don't exist."""
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Saved briefs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            persona TEXT NOT NULL,
            competitors TEXT,
            brief_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()


def hash_password(password: str) -> str:
    """Hash a password using SHA256 (simple, for demo - use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    return hash_password(password) == password_hash


def create_user(username: str, password: str) -> bool:
    """
    Create a new user.
    
    Returns:
        True if user was created, False if username already exists
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Username already exists
        return False
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[int]:
    """
    Authenticate a user.
    
    Returns:
        User ID if authentication successful, None otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user["password_hash"]):
        return user["id"]
    return None


def save_brief(user_id: int, company: str, persona: str, competitors: List[str], brief_content: str) -> int:
    """
    Save a brief for a user.
    
    Returns:
        The ID of the saved brief
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    title = f"{company} - {persona}"
    competitors_str = json.dumps(competitors)
    
    cursor.execute("""
        INSERT INTO saved_briefs (user_id, title, company, persona, competitors, brief_content)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, company, persona, competitors_str, brief_content))
    
    brief_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return brief_id


def get_user_briefs(user_id: int) -> List[Dict]:
    """Get all saved briefs for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, company, persona, competitors, created_at
        FROM saved_briefs
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    
    briefs = []
    for row in cursor.fetchall():
        briefs.append({
            "id": row["id"],
            "title": row["title"],
            "company": row["company"],
            "persona": row["persona"],
            "competitors": json.loads(row["competitors"]) if row["competitors"] else [],
            "created_at": row["created_at"]
        })
    
    conn.close()
    return briefs


def get_brief_content(brief_id: int, user_id: int) -> Optional[str]:
    """Get the full content of a saved brief."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT brief_content FROM saved_briefs
        WHERE id = ? AND user_id = ?
    """, (brief_id, user_id))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row["brief_content"]
    return None


def delete_brief(brief_id: int, user_id: int) -> bool:
    """Delete a saved brief."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM saved_briefs
        WHERE id = ? AND user_id = ?
    """, (brief_id, user_id))
    
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted
