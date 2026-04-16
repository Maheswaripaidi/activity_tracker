import sqlite3
from datetime import datetime
import os
import sys

#  Fix database path (works for EXE + Python)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

DB_NAME = os.path.join(BASE_DIR, "database.db")


#  Helper function (clean connection handling)
def get_connection():
    return sqlite3.connect(DB_NAME)


#  Initialize database
def init_db():
    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                details TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT,
                start_time TEXT,
                end_time TEXT,
                duration INTEGER
            )
        """)

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"DB Init Error: {e}")


#  Log event
def log_event(event_type, details=""):
    try:
        conn = get_connection()
        c = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute(
            "INSERT INTO events (timestamp, event_type, details) VALUES (?, ?, ?)",
            (timestamp, event_type, details)
        )

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Log Event Error: {e}")


#  Log app usage
def log_app_usage(app_name, start_time, end_time, duration):
    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
            INSERT INTO app_usage (app_name, start_time, end_time, duration)
            VALUES (?, ?, ?, ?)
        """, (app_name, start_time, end_time, duration))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Log App Usage Error: {e}")


#  Get events
def get_events():
    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("SELECT timestamp, event_type, details FROM events ORDER BY id")
        rows = c.fetchall()

        conn.close()
        return rows

    except Exception as e:
        print(f"Get Events Error: {e}")
        return []


# Get app usage
def get_app_usage():
    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("""
            SELECT app_name, SUM(duration)
            FROM app_usage
            GROUP BY app_name
        """)
        rows = c.fetchall()

        conn.close()
        return rows

    except Exception as e:
        print(f"Get App Usage Error: {e}")
        return []


#  Clear database (VERY IMPORTANT for fresh session)
def clear_database():
    try:
        conn = get_connection()
        c = conn.cursor()

        c.execute("DELETE FROM events")
        c.execute("DELETE FROM app_usage")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Clear DB Error: {e}")