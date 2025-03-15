import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('conversations.db')

# Crear un cursor
c = conn.cursor()

# Crear una tabla
c.execute('''CREATE TABLE IF NOT EXISTS conversations
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              role TEXT,
              content TEXT)''')

# Confirmar cambios y cerrar la conexión
conn.commit()
conn.close()