from db import get_conn, create_tables

create_tables()
conn = get_conn()
c = conn.cursor()

octavos = [
    ("Octavos","Real Madrid",1.4),
    ("Octavos","Man City",1.3),
    ("Octavos","PSG",1.9),
    ("Octavos","Inter",2.5)
]

for r,t,o in octavos:
    c.execute("INSERT INTO teams(round,team,odds) VALUES(?,?,?)",(r,t,o))

conn.commit()
print("Equipos cargados")
