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

¡Vamos con otro clásico de pruebas técnicas! Este ejercicio pone a prueba el manejo de estructuras de datos y lógica algorítmica.  

---

### **Ejercicio: Anagramas**  

Dadas dos cadenas de texto, escribe una función en Python que determine si son **anagramas**.  

#### **Requisitos:**  
1. Dos palabras son **anagramas** si tienen las mismas letras en distinta posición.  
2. La comparación **no debe ser sensible a mayúsculas/minúsculas**.  
3. Ignorar los espacios y caracteres especiales.  
4. La solución debe ser **eficiente (O(n))**.  

---

**Ejemplo de entrada:**  
```python
cadena1 = "Listen"
cadena2 = "Silent"
```
**Salida esperada:**  
```
Son anagramas: True
```

Otro ejemplo:  
```python
cadena1 = "Hello"
cadena2 = "Olelh"
```
**Salida esperada:**  
```
Son anagramas: True
```

---

### **Solución (O(n))**  

```python
from collections import Counter
import re

def son_anagramas(cadena1, cadena2):
    # Normalizar: convertir a minúsculas y eliminar caracteres que no sean letras
    cadena1 = re.sub(r'[^a-z]', '', cadena1.lower())
    cadena2 = re.sub(r'[^a-z]', '', cadena2.lower())

    # Comparar las frecuencias de letras usando Counter
    return Counter(cadena1) == Counter(cadena2)

# Ejemplo de uso
cadena1 = "Listen"
cadena2 = "Silent"
print(f"Son anagramas: {son_anagramas(cadena1, cadena2)}")
```

---

### **Explicación:**  
1. **Normalización de cadenas:**  
   - Convertimos a minúsculas (`lower()`).  
   - Eliminamos espacios y caracteres especiales usando `re.sub(r'[^a-z]', '', texto)`.  
2. **Comparación eficiente con `Counter` de `collections`**:  
   - Cuenta la frecuencia de cada letra en ambas cadenas.  
   - Si los `Counter` son iguales, las palabras son anagramas.  

---

### **Eficiencia:**  
✅ **Tiempo O(n)** (un solo recorrido para limpiar y otro para contar letras).  
✅ **Espacio O(1)** (uso mínimo de memoria adicional).  

---

Este ejercicio es muy común en pruebas técnicas para evaluar **manejo de cadenas, estructuras de datos y optimización**.  

🔥 ¿Te gustaría un nivel más difícil, como encontrar **todos los anagramas posibles en una lista de palabras**? 🚀

"""


format_markdown(md_content)
