def format_markdown(md_text):
    """
    Formatea texto Markdown eliminando líneas con '---', ajustando saltos de párrafo,
    eliminando etiquetas de lenguaje después de '```' (como 'bash') y manejando comillas internas.
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

        # Si la línea no está vacía y la anterior tampoco, añadir doble salto
        if i > 0 and stripped_line and lines[i-1].strip() and not stripped_line.startswith("```"):
            if formatted_lines and not formatted_lines[-1].endswith("\\n\\n"):
                formatted_lines[-1] = formatted_lines[-1].replace("\\n", "\\n\\n")

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

# **📌 Microservicios en Python: Guía completa con ejemplo práctico**  

## **¿Qué son los microservicios?**  
Los **microservicios** son un enfoque arquitectónico para desarrollar aplicaciones como un conjunto de **servicios pequeños, independientes y comunicados entre sí**. Cada microservicio tiene una responsabilidad específica y funciona de manera autónoma.  

🔹 **Características principales:**  
✅ **Independencia**: Cada servicio opera de forma autónoma.  
✅ **Escalabilidad**: Se pueden escalar individualmente.  
✅ **Despliegue independiente**: Cada servicio se puede actualizar sin afectar a otros.  
✅ **Comunicación entre servicios**: Generalmente mediante **APIs REST, gRPC o mensajería** (RabbitMQ, Kafka, Redis).  
✅ **Flexibilidad tecnológica**: Diferentes microservicios pueden usar distintos lenguajes o bases de datos.  

---

## **📌 Microservicios en un entorno Python**  
Python es una excelente opción para microservicios debido a su **sencillez y ecosistema**. Las herramientas más utilizadas son:  

🔹 **Frameworks web:**  
- [FastAPI](https://fastapi.tiangolo.com/) 🚀 (el más rápido)  
- [Flask](https://flask.palletsprojects.com/) 🏗️ (ligero y flexible)  
- [Django REST Framework (DRF)](https://www.django-rest-framework.org/) 🛠️ (ideal si usas Django)  

🔹 **Comunicación entre microservicios:**  
- **HTTP REST APIs** (con FastAPI, Flask, DRF).  
- **Mensajería asíncrona** con **RabbitMQ, Kafka, Redis Pub/Sub**.  
- **gRPC** (alta velocidad en comunicación binaria).  

🔹 **Gestión de microservicios:**  
- **Docker** (para contenerización).  
- **Kubernetes** (para orquestación de servicios).  
- **Consul o etcd** (para descubrimiento de servicios).  

---

## **📌 Ejemplo práctico de microservicio con Python y FastAPI**  
### 🏗 **Caso de uso:**  
Construiremos un **sistema de pedidos** con dos microservicios:  
1️⃣ **Microservicio de Usuarios** (`users_service.py`)  
2️⃣ **Microservicio de Pedidos** (`orders_service.py`)  

Los servicios se comunicarán entre sí mediante **HTTP REST APIs**.

---

### **1️⃣ Microservicio de Usuarios (`users_service.py`)**
Este servicio gestiona usuarios y expone un endpoint para obtener información de un usuario.  

```python
from fastapi import FastAPI

app = FastAPI()

# Base de datos simulada
users_db = {
    1: {"id": 1, "nombre": "Alice"},
    2: {"id": 2, "nombre": "Bob"}
}

@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int):
    usuario = users_db.get(user_id)
    if usuario:
        return usuario
    return {"error": "Usuario no encontrado"}, 404

# Ejecutar con: uvicorn users_service:app --reload --port 8001
```
📌 **Explicación:**  
✔️ **Usamos FastAPI** para exponer un endpoint `/usuarios/{user_id}`.  
✔️ **Simulamos una base de datos** en `users_db`.  
✔️ Si el usuario existe, lo devolvemos en JSON.  

---

### **2️⃣ Microservicio de Pedidos (`orders_service.py`)**
Este servicio gestiona pedidos y consulta el **microservicio de usuarios** para obtener información de los clientes.

```python
from fastapi import FastAPI
import requests  # Para comunicarnos con el otro microservicio

app = FastAPI()

# Base de datos simulada de pedidos
orders_db = {
    1: {"id": 1, "user_id": 1, "producto": "Laptop"},
    2: {"id": 2, "user_id": 2, "producto": "Teléfono"}
}

USER_SERVICE_URL = "http://127.0.0.1:8001/usuarios"  # URL del microservicio de usuarios

@app.get("/pedidos/{order_id}")
def obtener_pedido(order_id: int):
    pedido = orders_db.get(order_id)
    if not pedido:
        return {"error": "Pedido no encontrado"}, 404

    # Llamamos al microservicio de usuarios
    user_response = requests.get(f"{USER_SERVICE_URL}/{pedido['user_id']}")
    
    if user_response.status_code == 200:
        pedido["cliente"] = user_response.json()
    else:
        pedido["cliente"] = {"error": "Usuario no encontrado"}

    return pedido

# Ejecutar con: uvicorn orders_service:app --reload --port 8002
```
📌 **Explicación:**  
✔️ Exponemos un endpoint `/pedidos/{order_id}` para consultar pedidos.  
✔️ Buscamos en `orders_db` el pedido solicitado.  
✔️ Llamamos al **microservicio de usuarios** (`users_service`) con `requests.get()`.  
✔️ Si el usuario existe, lo agregamos a la respuesta del pedido.  

---

## **📌 Probando los microservicios**
### **1️⃣ Iniciar ambos microservicios en terminales separadas**
```bash
uvicorn users_service:app --reload --port 8001
```
```bash
uvicorn orders_service:app --reload --port 8002
```

### **2️⃣ Probar el servicio de Usuarios**
```bash
curl http://127.0.0.1:8001/usuarios/1
```
**Respuesta esperada:**
```json
{"id": 1, "nombre": "Alice"}
```

### **3️⃣ Probar el servicio de Pedidos**
```bash
curl http://127.0.0.1:8002/pedidos/1
```
**Respuesta esperada:**
```json
{
    "id": 1,
    "user_id": 1,
    "producto": "Laptop",
    "cliente": {
        "id": 1,
        "nombre": "Alice"
    }
}
```
📌 **¡Éxito!** El servicio de pedidos obtiene información del usuario llamando al otro microservicio.  

---

## **📌 Ventajas y Desventajas de Microservicios**
🔹 **Ventajas:**  
✅ Escalabilidad independiente de cada servicio.  
✅ Despliegue modular y flexible.  
✅ Menor acoplamiento (cada servicio se puede desarrollar y mantener por separado).  

🔹 **Desventajas:**  
❌ Mayor complejidad en la comunicación entre servicios.  
❌ Necesidad de gestionar la orquestación con herramientas como **Kubernetes**.  
❌ Requiere **observabilidad** con herramientas como **Prometheus y Grafana** para monitoreo.  

---

## **📌 Herramientas para Microservicios en Python**
✔️ **FastAPI / Flask / Django REST Framework** → Para construir APIs.  
✔️ **Docker & Kubernetes** → Para contenerización y despliegue.  
✔️ **RabbitMQ / Kafka / Redis** → Para comunicación asíncrona entre servicios.  
✔️ **PostgreSQL / MongoDB / Redis** → Bases de datos para almacenamiento.  
✔️ **Celery** → Para tareas en segundo plano.  

---

## **🎯 Conclusión**
🚀 **Los microservicios permiten crear aplicaciones escalables y modulares.**  
🔥 Python, junto con **FastAPI**, Docker y Kubernetes, es ideal para implementarlos.  
🔗 ¡Ahora tienes la base para diseñar tus propios microservicios en Python! 🚀

"""


format_markdown(md_content)
