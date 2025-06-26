import streamlit as st
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from app import DatabaseHandler

st.title("Wartości odstające")
st.text('Chcąc przejść do analizy danych, najpierw można zająć się detekcją i wykluczeniem wartości odstających.'
        'Stosuje się różne metody, ale tutaj zaprezentowany zostanie algorytm DBSCAN. Przyjmuje on takie argumenty'
        'jak eps oznaczający odległość w zdefiniowanej metryce, w której chcemy znaleźć min_samples, czyli minimalną liczbę'
        'punktów. Do znajdowania odpowiedniego parametru eps, można stworzyć wykres odległości do określonej liczby '
        'sąsiadów. Naszą odległością powinna być wartość, dla której wykres ma najwiekszy wzrost.')

baza = DatabaseHandler('pingwiny_db.db')
#conn = sqlite3.connect("pingwiny_db.db")
#df = pd.read_sql('SELECT * FROM pingwiny', conn)
df = baza.load_table('pingwiny')
df = df.dropna(subset=['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g'])

if "df" not in st.session_state:
    st.session_state.df = df
    st.session_state.labels = None
    st.session_state.df_cleaned = None

x = df[['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']]
x = StandardScaler().fit_transform(x)

neigh = NearestNeighbors(n_neighbors=8)
nbrs = neigh.fit(x)
distances, indices = nbrs.kneighbors(x)
distances = np.sort(distances, axis=0)
distances = distances[:, 1]
st.line_chart(distances)

eps = st.number_input("Wprowadź wartość eps, dla którego chcesz uruchomić algorytm DBSCAN i wybrać wartości odstające: ", value=0.8)
min_samples = st.number_input("Wprowadź minimalną liczbę próbek: ", min_value=1, max_value=350, value=8)

if st.button("Uruchom DBSCAN"):
    st.balloons()
    x = st.session_state.df[['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']]  # tylko kolumny numeryczne
    x = StandardScaler().fit_transform(x)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(x)
    st.session_state.df["label"] = labels
    st.session_state.labels = labels
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    st.text("Estymowana liczba klastrów: %d" % n_clusters_)
    st.text("Liczba obserwacji zaklasyfikowanych jako szum: %d" % n_noise_)
    st.success("DBSCAN zakończony.", icon="✅")

# Drugi przycisk: usuń obserwacje odstające
if st.session_state.labels is not None:
    if st.button("Usuń obserwacje odstające"):
        df_cleaned = st.session_state.df[st.session_state.df["label"] != -1].copy()
        st.session_state.df_cleaned = df_cleaned
        st.success("Usunięto obserwacje odstające.", icon="✅")
        st.write(f"Liczba pozostałych obserwacji: {len(df_cleaned)}")
        #df_cleaned.to_sql('pingwiny_zmodyfikowane', conn, if_exists='replace', index=False)
        baza.upload_table(df_cleaned, 'pingwiny_zmodyfikowane')

#conn.close()
