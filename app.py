import streamlit as st
from db import get_conn, create_tables
from game_logic import process_round

create_tables()
conn = get_conn()
c = conn.cursor()

st.title("🏆 Champions Survivor")

menu = st.sidebar.selectbox("Menu",["Registro","Jugar","Tabla","Admin"])

# REGISTRO
if menu=="Registro":
    name = st.text_input("Nombre")
    if st.button("Entrar"):
        try:
            c.execute("INSERT INTO players(name) VALUES(?)",(name,))
            conn.commit()
            st.success("Jugador creado")
        except:
            st.error("Ese nombre ya existe")

# JUGAR
if menu=="Jugar":
    player = st.selectbox("Jugador",[x[0] for x in c.execute("SELECT name FROM players")])
    round_name = "Octavos"

    used = [x[0] for x in c.execute("""
        SELECT team FROM picks 
        JOIN players ON picks.player_id=players.id 
        WHERE players.name=?
    """,(player,))]

    teams = [x[0] for x in c.execute("SELECT team FROM teams WHERE round=?",(round_name,)) if x[0] not in used]

    choice = st.selectbox("Equipo",teams)

    if st.button("Confirmar"):
        pid = c.execute("SELECT id FROM players WHERE name=?",(player,)).fetchone()[0]
        c.execute("INSERT INTO picks VALUES(?,?,?)",(pid,round_name,choice))
        conn.commit()
        st.success("Pick guardado")

# TABLA
if menu=="Tabla":
    st.table(c.execute("SELECT name,lives,points FROM players").fetchall())

# ADMIN
if menu=="Admin":
    st.subheader("Marcar ganadores")
    for t in c.execute("SELECT team FROM teams WHERE round='Octavos'"):
        if st.checkbox(t[0]):
            c.execute("UPDATE teams SET alive=1 WHERE team=?",(t[0],))
        else:
            c.execute("UPDATE teams SET alive=0 WHERE team=?",(t[0],))
    if st.button("Cerrar ronda"):
        process_round("Octavos")
        st.success("Ronda procesada")
