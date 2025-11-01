# generate_embeddings.py
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm  # barra de progreso (pip install tqdm)

DB_PATH = "my_database.sqlite"   # base de datos correcta
MODEL_NAME = "all-MiniLM-L6-v2"  # modelo local rápido

print("Cargando modelo de embeddings...")
model = SentenceTransformer(MODEL_NAME)

print("Conectando a base de datos...")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Procesar tabla python_db
print("Procesando tabla python_db...")
cur.execute("PRAGMA table_info(python_db)")
cols = [r[1] for r in cur.fetchall()]
if "embedding" not in cols:
    print("Agregando columna 'embedding' a python_db...")
    cur.execute("ALTER TABLE python_db ADD COLUMN embedding TEXT")
    conn.commit()

# Obtener filas sin embedding de python_db
cur.execute("SELECT id, prompt FROM python_db WHERE embedding IS NULL OR embedding = ''")
rows = cur.fetchall()

print(f"Generando embeddings para {len(rows)} registros en python_db...")
for row in tqdm(rows):
    _id, prompt = row
    try:
        emb = model.encode(prompt, normalize_embeddings=True)
        emb_json = str(emb.tolist())  # Guardar como string JSON
        cur.execute("UPDATE python_db SET embedding = ? WHERE id = ?", (emb_json, _id))
    except Exception as e:
        print(f"⚠️ Error en ID {_id}: {e}")

# Procesar tabla history
print("Procesando tabla history...")
cur.execute("PRAGMA table_info(history)")
cols = [r[1] for r in cur.fetchall()]
if "embedding" not in cols:
    print("Agregando columna 'embedding' a history...")
    cur.execute("ALTER TABLE history ADD COLUMN embedding TEXT")
    conn.commit()

# Obtener filas sin embedding de history
cur.execute("SELECT id, prompt FROM history WHERE embedding IS NULL OR embedding = ''")
rows = cur.fetchall()

print(f"Generando embeddings para {len(rows)} registros en history...")
for row in tqdm(rows):
    _id, prompt = row
    try:
        emb = model.encode(prompt, normalize_embeddings=True)
        emb_json = str(emb.tolist())  # Guardar como string JSON
        cur.execute("UPDATE history SET embedding = ? WHERE id = ?", (emb_json, _id))
    except Exception as e:
        print(f"⚠️ Error en ID {_id}: {e}")

conn.commit()
conn.close()
print("Embeddings generados y guardados correctamente.")
