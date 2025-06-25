import pandas as pd
import sqlite3

conn = sqlite3.connect("pingwiny_db.db")
cursor = conn.cursor()

# Tworzenie tabeli (jeśli nie istnieje)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pingwiny (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT,
    island TEXT,
    culmen_length_mm REAL,
    culmen_depth_mm REAL,
    flipper_length_mm REAL,
    body_mass_g REAL, 
    sex TEXT
)
""")
df = pd.read_csv("penguins_size.csv", delimiter=',')

conn = sqlite3.connect("pingwiny_db.db")

df.to_sql("pingwiny", conn, if_exists="replace", index=False)

conn.close()

print("Baza danych SQLite została utworzona.")
