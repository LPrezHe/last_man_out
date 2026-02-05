from db import get_conn, create_tables

create_tables()
conn = get_conn()
c = conn.cursor()

octavos = [
    ("Playoffs","Real Madrid",1),
    ("Playoffs","Benfica",1),
    ("Playoffs","PSG",1),
    ("Playoffs","Monaco",1),
    ("Playoffs","Newcastle",1),
    ("Playoffs","Qarabag",1),
    ("Playoffs","Atalanta",1),
    ("Playoffs","Dortmund",1)
    
]

for r,t,o in octavos:
    c.execute("INSERT INTO teams(round,team,odds) VALUES(?,?,?)",(r,t,o))

conn.commit()
print("Equipos cargados")
