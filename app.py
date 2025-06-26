# import numpy as np
import sqlite3
import pandas as pd
import streamlit as st

st.title("Analiza danych dotycząca pingwinów")
st.caption("projekt z przedmiotu programowanie w języku wysokiego poziomu II")
st.subheader('Wizualzacja danych')
st.text('Na początek zanim zjamiemy się analizą danych powinniśmy je sobie zwizualizować')
atrybuty = st.multiselect("Wybierz, dla których atrybutów chcesz zobaczyć wizualizację:",
                          ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"])

conn = sqlite3.connect("pingwiny_db.db")
df = pd.read_sql('SELECT * FROM pingwiny', conn)
df = df.dropna(subset=['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g'])

if len(atrybuty) == 2:
    st.subheader(f"Wykres {atrybuty} ")
    st.scatter_chart(df, x=atrybuty[0], y=atrybuty[1], color='species')

conn.close()
