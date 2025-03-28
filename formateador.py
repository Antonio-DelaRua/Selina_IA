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

## **Solución Paso a Paso**  

### **Paso 1: Importar las librerías necesarias**  
Python tiene una librería llamada `csv` que facilita la lectura y escritura de archivos CSV.  

```python
import csv
from collections import defaultdict
```

- `csv`: Nos permite manejar archivos CSV de manera sencilla.  
- `defaultdict`: Nos ayuda a almacenar datos sin necesidad de inicializar manualmente valores por defecto.  

---

### **Paso 2: Leer el archivo CSV y procesar los datos**  
Vamos a leer el archivo `ventas.csv` y almacenar los datos en un diccionario.  

```python
ventas = defaultdict(lambda: {"cantidad": 0, "ingresos": 0})  

with open("ventas.csv", newline='', encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    next(lector_csv)  # Omitimos la primera fila (encabezado)
    
    for fila in lector_csv:
        producto, cantidad, precio = fila[0], int(fila[1]), float(fila[2])
        
        # Acumulamos las cantidades y los ingresos
        ventas[producto]["cantidad"] += cantidad
        ventas[producto]["ingresos"] += cantidad * precio
```

### 🔹 **Explicación:**  
- Usamos `defaultdict` para crear un diccionario donde cada producto tiene sus ventas y sus ingresos acumulados.  
- Abrimos el archivo CSV en modo lectura (`open("ventas.csv", "r")`).  
- `csv.reader(archivo)` lee cada línea del archivo como una lista.  
- `next(lector_csv)` salta la primera fila porque es el encabezado.  
- Iteramos sobre cada fila, obteniendo:  
  - `producto` (nombre del producto)  
  - `cantidad` (convertida a entero)  
  - `precio` (convertido a flotante)  
- Acumulamos la cantidad total vendida y los ingresos en el diccionario `ventas`.  

---

### **Paso 3: Encontrar el producto más vendido y el de mayores ingresos**  

```python
producto_mas_vendido = max(ventas.items(), key=lambda x: x[1]["cantidad"])
producto_mas_ingresos = max(ventas.items(), key=lambda x: x[1]["ingresos"])

print(f"Producto más vendido: {producto_mas_vendido[0]} ({producto_mas_vendido[1]['cantidad']} unidades)")
print(f"Producto con más ingresos: {producto_mas_ingresos[0]} (${producto_mas_ingresos[1]['ingresos']:.2f})")
```

### 🔹 **Explicación:**  
- `max(ventas.items(), key=lambda x: x[1]["cantidad"])`: Busca el producto con mayor cantidad vendida.  
- `max(ventas.items(), key=lambda x: x[1]["ingresos"])`: Encuentra el producto con más ingresos.  
- `print()`: Muestra los resultados en la consola.  

---

### **Paso 4: Guardar los resultados en un nuevo archivo CSV**  

```python
with open("resultados_ventas.csv", "w", newline='', encoding='utf-8') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida)
    
    # Escribir encabezado
    escritor_csv.writerow(["Producto", "Cantidad Vendida", "Ingresos Totales"])
    
    # Escribir datos
    for producto, datos in ventas.items():
        escritor_csv.writerow([producto, datos["cantidad"], f"{datos['ingresos']:.2f}"])
```

### 🔹 **Explicación:**  
- Abrimos un nuevo archivo `resultados_ventas.csv` en modo escritura.  
- Escribimos la primera fila con los nombres de las columnas.  
- Iteramos sobre el diccionario `ventas` para escribir los datos en el archivo.  

---

## **Código Completo**  

```python
import csv
from collections import defaultdict

# Diccionario para almacenar los datos
ventas = defaultdict(lambda: {"cantidad": 0, "ingresos": 0})

# Leer archivo CSV y procesar datos
with open("ventas.csv", newline='', encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    next(lector_csv)  # Saltar el encabezado

    for fila in lector_csv:
        producto, cantidad, precio = fila[0], int(fila[1]), float(fila[2])
        ventas[producto]["cantidad"] += cantidad
        ventas[producto]["ingresos"] += cantidad * precio

# Encontrar productos destacados
producto_mas_vendido = max(ventas.items(), key=lambda x: x[1]["cantidad"])
producto_mas_ingresos = max(ventas.items(), key=lambda x: x[1]["ingresos"])

print(f"Producto más vendido: {producto_mas_vendido[0]} ({producto_mas_vendido[1]['cantidad']} unidades)")
print(f"Producto con más ingresos: {producto_mas_ingresos[0]} (${producto_mas_ingresos[1]['ingresos']:.2f})")

# Guardar los resultados en un nuevo archivo CSV
with open("resultados_ventas.csv", "w", newline='', encoding='utf-8') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida)
    escritor_csv.writerow(["Producto", "Cantidad Vendida", "Ingresos Totales"])

    for producto, datos in ventas.items():
        escritor_csv.writerow([producto, datos["cantidad"], f"{datos['ingresos']:.2f}"])
```

---

## **Ejemplo de Salida en Consola**  

```
Producto más vendido: Teclado (15 unidades)
Producto con más ingresos: Laptop ($4900.00)
```

## **Ejemplo de Salida en `resultados_ventas.csv`**  

```
Producto,Cantidad Vendida,Ingresos Totales
Laptop,7,4900.00
Teclado,15,300.00
Mouse,8,120.00
Monitor,4,600.00
```

---

## **¿Qué se aprende con este ejercicio?**  
✅ **Manejo de archivos CSV** (lectura y escritura).  
✅ **Uso de estructuras de datos avanzadas** (`defaultdict` para acumular información).  
✅ **Uso de funciones de ordenación** (`max()` con `lambda`).  
✅ **Bucles e iteraciones eficientes**.  
✅ **Conversión de tipos de datos** (de cadena a `int` y `float`).  


"""


format_markdown(md_content)
