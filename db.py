import sqlite3

def get_conn():
    return sqlite3.connect("survivor.db", check_same_thread=False)

def create_tables():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    password TEXT,
    lives INTEGER DEFAULT 3,
    points REAL DEFAULT 0
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS picks (
        player_id INTEGER,
        round TEXT,
        team TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        round TEXT,
        team TEXT,
        odds REAL,
        alive INTEGER DEFAULT 1
    )
    """)

    conn.commit()
