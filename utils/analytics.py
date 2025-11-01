import sqlite3
import os
import json

# === Путь к базе данных ===
DB_PATH = os.path.join(os.path.dirname(__file__), "analytics.db")

# === Инициализация базы данных ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            event_type TEXT,
            event_name TEXT,
            payload TEXT,
            chapter TEXT,
            meta TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# === Функция для логирования событий ===
def log_event(user_id, username=None, first_name=None, last_name=None,
              event_type=None, event_name=None, payload=None, chapter=None, meta=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (
            user_id, username, first_name, last_name,
            event_type, event_name, payload, chapter, meta
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        username,
        first_name,
        last_name,
        event_type,
        event_name,
        payload,
        chapter,
        json.dumps(meta) if meta else None
    ))
    conn.commit()
    conn.close()

# === Автоинициализация при импорте ===
init_db()
