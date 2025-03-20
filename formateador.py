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


¡Claro! **Markdown** es un lenguaje ligero de marcado que se usa para dar formato a textos de manera sencilla. Aunque no está directamente relacionado con **Python**, puedes usar **Markdown** para documentar código Python en archivos como `README.md`, en **Jupyter Notebooks**, o en plataformas como **GitHub**. Aquí tienes una guía con los comandos más usados en **Markdown** y cómo aplicarlos para documentar tus proyectos en Python:

---

## 📋 **Guía de comandos Markdown**

### 1. **Encabezados (Títulos)**  
Se crean usando el símbolo `#` seguido de un espacio.

```markdown
# Título de nivel 1
## Título de nivel 2
### Título de nivel 3
```

📝 **Ejemplo en Python**:
```markdown
# Proyecto de Python: Calculadora
## Descripción
Este programa realiza operaciones básicas: suma, resta, multiplicación y división.
```

---

### 2. **Negrita y Cursiva**
- **Negrita**: Usa `**texto**` o `__texto__`
- *Cursiva*: Usa `*texto*` o `_texto_`
- ***Negrita y cursiva***: Usa `***texto***`

📝 **Ejemplo en Python**:
```markdown
**Función principal**
*Este programa está desarrollado en Python 3.*
```

---

### 3. **Código en línea y bloques de código**
- **Código en línea**: Usa una comilla invertida \(`)
- **Bloque de código**: Usa tres comillas invertidas (\`\`\`) con el lenguaje especificado.

📝 **Ejemplo en Python**:
```markdown
Llama a la función con:

```python
suma(2, 3)
```
```

---

### 4. **Listas**
- **Lista no ordenada**: Usa `-`, `*` o `+`
- **Lista ordenada**: Usa números seguidos de un punto (`1.`, `2.`, etc.)

📝 **Ejemplo en Python**:
```markdown
### Funciones implementadas:

- Sumar
- Restar
- Multiplicar
- Dividir

### Pasos para ejecutar:
1. Clonar el repositorio
2. Instalar dependencias
3. Ejecutar `main.py`
```

---

### 5. **Enlaces e Imágenes**
- **Enlace**: `[Texto del enlace](URL)`
- **Imagen**: `![Texto alternativo](ruta/imagen.png)`

📝 **Ejemplo en Python**:
```markdown
[Documentación oficial de Python](https://www.python.org)

![Logo de Python](https://www.python.org/static/community_logos/python-logo.png)
```

---

### 6. **Tablas**
Para crear tablas, usa el símbolo `|` para las columnas y `-` para dividir el encabezado del contenido.

📝 **Ejemplo en Python**:
```markdown
| Función      | Descripción               |
|--------------|---------------------------|
| `suma()`     | Realiza una suma          |
| `resta()`    | Realiza una resta         |
| `multiplica()` | Multiplica dos números    |
| `divide()`   | Divide dos números         |
```

---

### 7. **Citas (Blockquotes)**
Usa el símbolo `>` al inicio de la línea.

📝 **Ejemplo en Python**:
```markdown
> Este proyecto está basado en Python 3.10.
```

---

### 8. **Líneas divisorias**
Se crean usando tres guiones `---`, asteriscos `***` o guiones bajos `___`.

```markdown
---
```

---

### 📚 **Ejemplo Completo en Markdown para Python**
```markdown
# 📊 Calculadora en Python

## 📌 Descripción
Este proyecto es una calculadora básica en **Python** que realiza operaciones como:

- Suma
- Resta
- Multiplicación
- División

## 🔧 Requisitos
- Python 3.10 o superior
- Librerías: Ninguna externa

## 📋 Uso

```python
# Ejecutar la calculadora
from calculadora import suma

resultado = suma(5, 3)
print(f"Resultado: {resultado}")
```

## 📄 Documentación
Para más detalles, consulta la [documentación oficial de Python](https://www.python.org).
```

---

¿Quieres que te ayude a crear un **README.md** para tu proyecto en Python? 🚀

"""


format_markdown(md_content)