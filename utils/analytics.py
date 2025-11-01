import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "analytics.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_id INTEGER,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        event_type TEXT,
        event_name TEXT,
        payload TEXT,
        chapter TEXT,
        meta TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_event(user_id, username=None, first_name=None, last_name=None,
              event_type=None, event_name=None, payload=None,
              chapter=None, meta=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO events (timestamp, user_id, username, first_name, last_name,
                        event_type, event_name, payload, chapter, meta)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        user_id,
        username,
        first_name,
        last_name,
        event_type,
        event_name,
        payload,
        chapter,
        str(meta) if meta else None
    ))
    conn.commit()
    conn.close()
