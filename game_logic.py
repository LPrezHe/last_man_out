import sqlite3
from db import get_conn

def process_round(round_name):
    conn = get_conn()
    c = conn.cursor()

    # Equipos que avanzan
    winners = c.execute(
        "SELECT team, odds FROM teams WHERE round=? AND alive=1",
        (round_name,)
    ).fetchall()

    winners = {t[0]: t[1] for t in winners}

    picks = c.execute("""
        SELECT p.id, p.name, pk.team 
        FROM picks pk
        JOIN players p ON pk.player_id = p.id
        WHERE pk.round=?
    """, (round_name,)).fetchall()

    for pid, name, team in picks:
        if team in winners:
            points = 1 / winners[team]
            c.execute("UPDATE players SET points = points + ? WHERE id=?", (points, pid))
        else:
            c.execute("UPDATE players SET lives = lives - 1 WHERE id=?", (pid,))

    conn.commit()
