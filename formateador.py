def format_markdown(md_text):
    """
    Formatea texto Markdown eliminando líneas con '---', ajustando saltos de párrafo,
    eliminando etiquetas de lenguaje después de '```' y manejando comillas internas.
    """
    lines = md_text.split("\n")
    formatted_lines = []
    skip_next_empty = False  # Para manejar saltos después de eliminar '---'

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # Eliminar líneas que solo contienen '---'
        if stripped_line == "---":
            skip_next_empty = True  # Indicar que el próximo salto debe ser manejado
            continue

        # Eliminar líneas vacías si la anterior fue un '---' eliminado
        if skip_next_empty and not stripped_line:
            continue
        skip_next_empty = False

        # Eliminar la etiqueta de lenguaje después de ```
        if stripped_line.startswith("```") and len(stripped_line) > 3:
            line = "```"

        # Manejar comillas internas
        if '"' in line:
            line = line.replace('"', "'")
        elif "'" in line:
            line = line.replace("'", '"')

        formatted_lines.append(f'"{line}\\n"')

    formatted_text = "\n".join(formatted_lines)

    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)

    print("Archivo formateado generado: formatted_output.txt")


# Ejemplo de entrada Markdown (tu contenido)
md_content = """

## 🚀 **¿Qué es uWSGI?**  
**uWSGI** es un servidor de aplicaciones **WSGI** que permite ejecutar aplicaciones Python (Flask, Django, FastAPI) en producción.  

🔹 **¿Por qué usar uWSGI?**  
✅ Es **rápido y eficiente**, con soporte para múltiples workers y threads.  
✅ Compatible con **Nginx y Apache** como proxy reverso.  
✅ Soporta múltiples protocolos (WSGI, HTTP, FastCGI, uWSGI, etc.).  
✅ Más configurable que Gunicorn, pero más complejo de usar.  

🔹 **Alternativas:**  
- **Gunicorn** (más simple y usado con Flask/Django).  
- **Daphne** (para Django con WebSockets).  
- **Uvicorn** (para FastAPI con ASGI).  

---

## 🛠️ **Ejemplo: Ejecutar Flask con uWSGI**  

📌 **1️⃣ Instalar uWSGI y Flask**  
```sh
pip install flask uwsgi
```

📌 **2️⃣ Crear la API en Flask**  
📄 **`app.py`**  

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola desde Flask con uWSGI!"

if __name__ == '__main__':
    app.run()
```

📌 **3️⃣ Ejecutar con uWSGI**  
```sh
uwsgi --http :8000 --wsgi-file app.py --callable app --processes 4 --threads 2
```
🔹 `--http :8000` → Escucha en el puerto `8000`.  
🔹 `--wsgi-file app.py` → Usa el archivo `app.py`.  
🔹 `--callable app` → La aplicación se llama `app`.  
🔹 `--processes 4` → Usa **4 procesos workers**.  
🔹 `--threads 2` → Cada proceso usa **2 threads**.  

📌 **4️⃣ Acceder a la API**  
Abre en el navegador:  
```
http://localhost:8000/
```

---

## 🔥 **uWSGI + Nginx (Producción)**  
En producción, se usa **Nginx** como proxy reverso para manejar peticiones y mejorar rendimiento.  

📄 **Configurar Nginx (`/etc/nginx/sites-available/default`)**  
```nginx
server {
    listen 80;

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
    }
}
```

📌 **Ejecutar uWSGI con socket Unix**  
```sh
uwsgi --socket /tmp/uwsgi.sock --wsgi-file app.py --callable app --processes 4 --threads 2 --chmod-socket=666
```

📌 **Reiniciar Nginx**  
```sh
sudo systemctl restart nginx
```

Ahora, Nginx manejará las peticiones y las enviará a uWSGI.

---

## 🎯 **¿Cuándo usar uWSGI?**  
✅ Cuando necesitas **alto rendimiento** y personalización.  
✅ Para ejecutar **Flask o Django en producción con Nginx**.  
✅ Cuando necesitas compatibilidad con **FastCGI, HTTP y WSGI**.  

---

🚀 **Ejemplo real:**  
Un **API REST en Flask** usa **uWSGI + Nginx** para manejar **miles de usuarios** con múltiples procesos y threads.  



"""


format_markdown(md_content)
