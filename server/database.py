import sqlite3
import os


DB_PATH = "data/battleship.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            total_match INTEGER DEFAULT 0,
            win INTEGER DEFAULT 0,
            lose INTEGER DEFAULT 0,
            hit_count INTEGER DEFAULT 0,
            miss_count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()