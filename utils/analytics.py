# utils/analytics.py
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "analytics.db"  # ../analytics.db

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
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

def log_event(user_id: int, event_type: str, event_name: str,
              payload: str = None, username: str = None,
              first_name: str = None, last_name: str = None,
              chapter: str = None, meta: dict | None = None):
    """
    Сохраняет событие в БД. meta — словарь, будет сериализован в JSON.
    """
    ts = datetime.utcnow().isoformat()
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO events (ts, user_id, username, first_name, last_name,
                            event_type, event_name, payload, chapter, meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, user_id, username, first_name, last_name,
          event_type, event_name, payload, chapter, meta_json))
    conn.commit()
    conn.close()

# Экспорт в CSV/XLSX
def export_csv(path: str = "events.csv"):
    import csv
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)

def export_xlsx(path: str = "events.xlsx"):
    # требует pandas and openpyxl
    import pandas as pd
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM events ORDER BY id", conn)
    conn.close()
    df.to_excel(path, index=False)
