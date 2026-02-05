import streamlit as st
from db import get_conn, create_tables
from game_logic import process_round
from auth import hash_password, verify_password
import os

if os.path.exists("survivor.db"):
    os.remove("survivor.db")

create_tables()
import seed
conn = get_conn()
c = conn.cursor()

st.title("🏆 Champions Last Man Out")

menu = st.sidebar.selectbox("Menu",["Registro","Jugar","Tabla","Admin","Login"])

if "user" not in st.session_state:
    st.session_state.user = None

# REGISTRO
if menu=="Registro":
    name = st.text_input("Usuario")
    password = st.text_input("Contraseña",type="password")

    if st.button("Crear cuenta"):
        if not name or not password:
            st.error("Completa todos los campos")
        else:
            hashed = hash_password(password)
            try:
                c.execute("INSERT INTO players(name,password) VALUES(?,?)",(name,hashed))
                conn.commit()
                st.success("Cuenta creada. Ahora puedes iniciar sesión.")
            except:
                st.error("Ese usuario ya existe")

if menu=="Login":
    name = st.text_input("Usuario")
    pw = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        data = c.execute("SELECT password FROM players WHERE name=?",(name,)).fetchone()
        if data and verify_password(pw, data[0]):
            st.session_state.user = name
            st.success("Bienvenido " + name)
        else:
            st.error("Login incorrecto")

# JUGAR
if menu=="Jugar":
    player = st.session_state.user
    if not player:
        st.warning("Debes iniciar sesión")
        st.stop()

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

    teams = c.execute("SELECT team, alive FROM teams WHERE round='Octavos'").fetchall()
    new_status = {}

    for team, alive in teams:
        new_status[team] = st.checkbox(team, value=bool(alive))

    if st.button("Guardar resultados"):
        for team, alive in new_status.items():
            c.execute("UPDATE teams SET alive=? WHERE team=?", (1 if alive else 0, team))
        conn.commit()
        st.success("Resultados guardados")

    if st.button("Cerrar ronda"):
        process_round("Octavos")
        st.success("Ronda procesada")
