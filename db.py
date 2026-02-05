import sqlite3

def get_conn():
    return sqlite3.connect("survivor.db", check_same_thread=False)

def create_tables():
    conn = get_conn()
    c = conn.cursor()

    # players
    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        password TEXT,
        lives INTEGER DEFAULT 3,
        points INTEGER DEFAULT 0
    )
    """)

    # Fix si la tabla vieja no tenía password
    try:
        c.execute("ALTER TABLE players ADD COLUMN password TEXT")
    except:
        pass

    # teams
    c.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        round TEXT,
        team TEXT,
        alive INTEGER
    )
    """)

    # picks
    c.execute("""
    CREATE TABLE IF NOT EXISTS picks (
        player_id INTEGER,
        round TEXT,
        team TEXT
    )
    """)

    conn.commit()
    conn.close()
