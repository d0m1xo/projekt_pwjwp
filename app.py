import sqlite3
import pandas as pd
import streamlit as st


class DatabaseHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def load_table(self, table_name: str):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)


st.title("Analiza danych dotycząca pingwinów")
st.caption("projekt z przedmiotu programowanie w języku wysokiego poziomu II")
st.subheader('Wizualzacja danych')
st.text('Na początek zanim zjamiemy się analizą danych, powinniśmy je sobie zwizualizować.'
        'Możemy wybierać kolumny z naszego zbioru danych, w odpowiedniej kolejności.')
atrybuty = st.multiselect("Wybierz, dla których atrybutów chcesz zobaczyć wizualizację:",
                          ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"])

baza = DatabaseHandler('pingwiny_db.db')
tabela = baza.load_table('pingwiny')
df = tabela.dropna(subset=['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g'])

legenda = st.pills("Wybierz jaki chcesz podział: ", ['species', 'sex'], default='species')

if len(atrybuty) == 2:
    st.subheader(f"Wykres {atrybuty} ")
    st.scatter_chart(df, x=atrybuty[0], y=atrybuty[1], color=legenda)
