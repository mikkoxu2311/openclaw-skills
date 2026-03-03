#!/usr/bin/env python3
"""
Database operations for Daily Journal skill.
SQLite database for caching daily entries.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".openclaw/workspace/skills/daily-journal/cache/journal.db"

def init_db():
    """Initialize database tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Entries table for general conversation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            phase TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Captures table for insights, ideas, seeds, fleeting notes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS captures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            tags TEXT,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Day interrupts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS day_interrupts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time_slot TEXT,
            doing TEXT,
            reflection TEXT,
            insight TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Morning setup table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS morning_setup (
            date TEXT PRIMARY KEY,
            energy_score INTEGER,
            focus_task TEXT,
            template TEXT,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Conversations table for project retrospectives and reflections
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            topic TEXT,
            summary TEXT,
            raw_content TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_conn():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)

# === Entries ===

def add_entry(date: str, phase: str, content: str):
    """Add a general entry."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (date, phase, content) VALUES (?, ?, ?)",
        (date, phase, content)
    )
    conn.commit()
    conn.close()

def get_entries(date: str):
    """Get all entries for a date."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT phase, content, created_at FROM entries WHERE date = ? ORDER BY created_at",
        (date,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# === Captures ===

def add_capture(date: str, cap_type: str, content: str, tags: list = None, context: str = None):
    """Add a capture (insight, idea, seed, fleeting)."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO captures (date, type, content, tags, context) VALUES (?, ?, ?, ?, ?)",
        (date, cap_type, content, json.dumps(tags or []), context)
    )
    conn.commit()
    conn.close()

def get_captures(date: str, cap_type: str = None):
    """Get captures for a date, optionally filtered by type."""
    conn = get_conn()
    cursor = conn.cursor()
    
    if cap_type:
        cursor.execute(
            "SELECT type, content, tags, context FROM captures WHERE date = ? AND type = ? ORDER BY created_at",
            (date, cap_type)
        )
    else:
        cursor.execute(
            "SELECT type, content, tags, context FROM captures WHERE date = ? ORDER BY created_at",
            (date,)
        )
    
    results = cursor.fetchall()
    conn.close()
    return results

# === Day Interrupts ===

def add_day_interrupt(date: str, time_slot: str, doing: str, reflection: str = None, insight: str = None):
    """Add a day interrupt check-in."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO day_interrupts (date, time_slot, doing, reflection, insight) VALUES (?, ?, ?, ?, ?)",
        (date, time_slot, doing, reflection, insight)
    )
    conn.commit()
    conn.close()

def get_day_interrupts(date: str):
    """Get all day interrupts for a date."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT time_slot, doing, reflection, insight FROM day_interrupts WHERE date = ? ORDER BY created_at",
        (date,)
    )
    results = cursor.fetchall()
    conn.close()
    return results

# === Morning Setup ===

def save_morning_setup(date: str, energy_score: int, focus_task: str, template: str, context: str = None):
    """Save morning setup."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT OR REPLACE INTO morning_setup 
           (date, energy_score, focus_task, template, context) 
           VALUES (?, ?, ?, ?, ?)''',
        (date, energy_score, focus_task, template, context)
    )
    conn.commit()
    conn.close()

def get_morning_setup(date: str):
    """Get morning setup for a date."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT energy_score, focus_task, template, context FROM morning_setup WHERE date = ?",
        (date,)
    )
    result = cursor.fetchone()
    conn.close()
    return result

# === Conversations (Project & Reflection) ===

def add_conversation(date: str, conv_type: str, topic: str = None, summary: str = None, 
                     raw_content: str = None, tags: list = None):
    """Save a conversational retrospective or reflection."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO conversations (date, type, topic, summary, raw_content, tags)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (date, conv_type, topic, summary, raw_content, json.dumps(tags or []))
    )
    conn.commit()
    conn.close()

def get_conversations(date: str, conv_type: str = None):
    """Get conversations for a date, optionally filtered by type."""
    conn = get_conn()
    cursor = conn.cursor()
    
    if conv_type:
        cursor.execute(
            "SELECT type, topic, summary, raw_content, tags FROM conversations WHERE date = ? AND type = ? ORDER BY created_at",
            (date, conv_type)
        )
    else:
        cursor.execute(
            "SELECT type, topic, summary, raw_content, tags FROM conversations WHERE date = ? ORDER BY created_at",
            (date,)
        )
    
    results = cursor.fetchall()
    conn.close()
    return results

# === Cleanup ===

def clear_date(date: str):
    """Clear all data for a date after archiving."""
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM entries WHERE date = ?", (date,))
    cursor.execute("DELETE FROM captures WHERE date = ?", (date,))
    cursor.execute("DELETE FROM day_interrupts WHERE date = ?", (date,))
    cursor.execute("DELETE FROM morning_setup WHERE date = ?", (date,))
    cursor.execute("DELETE FROM conversations WHERE date = ?", (date,))
    
    conn.commit()
    conn.close()

def has_data(date: str) -> bool:
    """Check if there's any data for a date."""
    conn = get_conn()
    cursor = conn.cursor()
    
    tables = ['entries', 'captures', 'day_interrupts', 'morning_setup', 'conversations']
    for table in tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE date = ? LIMIT 1", (date,))
        if cursor.fetchone():
            conn.close()
            return True
    
    conn.close()
    return False

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
