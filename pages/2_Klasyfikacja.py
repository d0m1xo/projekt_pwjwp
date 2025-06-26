import streamlit as st
import sqlite3
import pandas as pd
import numpy as npimport
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

st.title("Klasyfikacja")
st.text('Znaleźliśmy już wartości odstające i pozbyliśmy się ich z naszego zbioru danych. Możemy zatem przejśc'
        'do prób tworzenia modeli klasyfikujących pingwiny na podstawie atrybutów.')

conn = sqlite3.connect("pingwiny_db.db")

try:
    df = pd.read_sql_query("SELECT * FROM pingwiny_zmodyfikowane", conn)
    st.text("Dane z usuniętymi wartościami odstającymi")
except Exception as e:
    df = pd.read_sql_query("SELECT * FROM pingwiny", conn)
    st.text("Dane pierwotne")

df = df.dropna(subset=['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g'])
conn.close()

x = df[['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']]
train_x, test_x, train_y, test_y = train_test_split(x, df['species'], test_size=0.2, random_state=42)
min_samples = st.number_input("Wprowadź liczbę sąsiiadów: ", min_value=1, max_value=350, value=4)
if st.button("Przeprowadź analizę"):
    st.balloons()
    neigh = KNeighborsClassifier(n_neighbors=min_samples, metric='cosine')
    nbrs = neigh.fit(train_x, train_y)
    cm = confusion_matrix(test_y, nbrs.predict(test_x))
    st.title("Wizualizacja Confusion Matrix")
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1], yticklabels=[0, 1])
    ax.set_xlabel('Przewidziane')
    ax.set_ylabel('Rzeczywiste')
    ax.set_title('Confusion Matrix')
    st.pyplot(fig)
