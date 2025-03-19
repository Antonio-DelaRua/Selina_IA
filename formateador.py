def format_markdown(md_text):
    """
    Formatea texto Markdown eliminando líneas con '---' y ajustando saltos de párrafo.
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
        
        # Si la línea no está vacía y la anterior tampoco, añadir doble salto
        if i > 0 and stripped_line and lines[i-1].strip() and not stripped_line.startswith("```"):
            if formatted_lines and not formatted_lines[-1].endswith("\\n\\n"):
                formatted_lines[-1] = formatted_lines[-1].replace("\\n", "\\n\\n")
        
        formatted_lines.append(f'"{line}\\n"')

    formatted_text = "\n".join(formatted_lines)
    
    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)
    
    print("Archivo formateado generado: formatted_output.txt")


# Ejemplo de entrada Markdown (tu contenido)
md_content = """


¡Claro! Aquí tienes una explicación de **Django** junto con ejemplos en **Markdown**:

---

# 🐍 **Django: El framework web en Python**

Django es un **framework de desarrollo web** de alto nivel y código abierto, diseñado para crear aplicaciones web de manera rápida, segura y escalable. Sigue el patrón **MTV (Model-Template-View)**, similar al **MVC (Model-View-Controller)**.

---

## ✅ **Principales características de Django**
- **Rápido**: Facilita un desarrollo ágil y limpio.
- **Seguro**: Incluye protección contra inyecciones SQL, CSRF, XSS, etc.
- **Escalable**: Adaptable a proyectos pequeños y grandes.
- **DRY (Don't Repeat Yourself)**: Reutilización de código y optimización.

---

## 📁 **Estructura básica de un proyecto Django**
```bash
mi_proyecto/
├── manage.py          # Utilidad para administrar el proyecto
├── mi_proyecto/       # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py    # Configuración principal
│   ├── urls.py        # Rutas del proyecto
│   └── wsgi.py        # Interfaz WSGI para producción
└── app/               # Una aplicación Django
    ├── __init__.py
    ├── admin.py      # Registro en el panel de administración
    ├── apps.py       # Configuración de la aplicación
    ├── models.py     # Definición de la base de datos (Modelos)
    ├── tests.py      # Pruebas unitarias
    └── views.py      # Lógica de las vistas
```

---

## 🚀 **Cómo empezar con Django**
### 1. **Instalar Django**
Asegúrate de tener Python instalado y ejecuta:
```bash
pip install django
```

### 2. **Crear un proyecto Django**
```bash
django-admin startproject mi_proyecto
cd mi_proyecto
python manage.py runserver
```
Accede a `http://localhost:8000` para ver la página de bienvenida.

---

## 📊 **Ejemplo: Crear una aplicación en Django**
### 1. Crear una aplicación:
```bash
python manage.py startapp blog
```

### 2. Registrar la app en `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'blog',
]
```

### 3. Definir un modelo en `models.py`:
```python
from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

### 4. Migrar la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear una vista en `views.py`:
```python
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("¡Hola, Django!")
```

### 6. Configurar la URL en `urls.py`:
```python
from django.urls import path
from blog.views import inicio

urlpatterns = [
    path('', inicio, name='inicio'),
]
```

---

## 🛠️ **Panel de administración de Django**
1. Crear un superusuario:
```bash
python manage.py createsuperuser
```

2. Registrar el modelo en `admin.py`:
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

3. Acceder al panel: `http://localhost:8000/admin`

---

## 📚 **Recursos adicionales**
- 📘 [Documentación oficial de Django](https://docs.djangoproject.com/)
- 🧰 **Comandos útiles**:
    ```bash
    python manage.py runserver       # Ejecutar el servidor
    python manage.py makemigrations  # Crear migraciones
    python manage.py migrate         # Aplicar migraciones
    python manage.py createsuperuser # Crear usuario administrador
    ```
---

¿Quieres que profundice en alguna parte o te muestre más ejemplos? 🚀


"""


format_markdown(md_content)