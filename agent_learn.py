from model import PythonDB

def add_or_update_predefined_prompt(prompt, response):
    try:
        # Verificar si el prompt ya existe
        existing_entry = PythonDB.get_by_prompt(prompt)
        if existing_entry:
            # Si el prompt existe, actualizar la respuesta
            existing_entry.response = response
            existing_entry.save()
            print(f"Prompt existente actualizado: {prompt} -> {response}")
        else:
            # Si el prompt no existe, crear una nueva entrada
            new_entry = PythonDB(prompt=prompt, response=response)
            new_entry.save()
            print(f"Nuevo prompt predefinido agregado: {prompt} -> {response}")
    except Exception as e:
        print(f"Error al agregar o actualizar el prompt predefinido: {e}")

if __name__ == "__main__":
    # Ejemplo de uso
    prompt = "¿Qué es una base de datos?"
    response = "Una base de datos es una colección organizada de datos, generalmente almacenados y accesibles electrónicamente desde un sistema informático."

    add_or_update_predefined_prompt(prompt, response)
    
    # Agregar más prompts predefinidos según sea necesario
    prompts_responses = [
            (
        "que es python y para que se utiliza?",
        "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. "
        "Es conocido por su sintaxis sencilla y legible, lo que facilita su aprendizaje y uso.\n\n"
        "¿Para qué se utiliza Python?\n"
        "Python es muy versátil y se usa en diversos campos, como:\n\n"
        "- **Desarrollo web**: Con frameworks como Django y Flask.\n"
        "- **Ciencia de datos y Machine Learning**: Con bibliotecas como NumPy, Pandas, TensorFlow y Scikit-learn.\n"
        "- **Automatización y scripting**: Para escribir scripts que automatizan tareas repetitivas.\n"
        "- **Ciberseguridad**: Para análisis forense y pruebas de penetración.\n"
        "- **Desarrollo de videojuegos**: Con motores como Pygame.\n"
        "- **Administración de sistemas**: Para gestionar servidores y redes.\n"
        "- **Aplicaciones de escritorio**: Usando Tkinter o PyQt.\n"
        "- **Internet de las Cosas (IoT)**: Para programar dispositivos inteligentes."
    ),

            (
        "como instalar python en windows?",
        "Para instalar Python en Windows, sigue estos pasos:\n\n"
        "**Descarga Python**\n"
        "- Ve al sitio web oficial de Python: https://www.python.org/downloads/ \n\n"
        "**Instala Python**\n"
        "- Abre el archivo descargado (python-xxx.exe).\n"
        "- IMPORTANTE: Marca la casilla 'Add Python to PATH' (Agregar Python al PATH).\n"
        "- Haz clic en 'Install Now' y espera a que termine la instalación.\n\n"
        "**Verifica la instalación**\n"
        "- Presiona Win + R, escribe cmd y presiona Enter.\n"
        "```\npython --version\n"
        "or python -V\n```\n\n"
        "**(OPCIONAL) Instalar pip y probarlo**\n"
        "```\npip --version\n```\n"
        "```\npip install numpy pandas\n```"
    ),

            (
        "fundamentos de python",
        "**Sintaxis y Semántica Básica:**\n\n"
        "- **Tipos de datos básicos:** [int]  |  [float]  | [str]  |  [bool] \n\n"
        "- **Operadores:** [aritméticos]  |  [comparativos]  |  [lógicos]\n\n"
        "- **Estructuras de control:** [if]  |  [for]  |  [while]\n"
    ),

 (
        "tipos de datos basicos",
        "Python es un lenguaje de programación de alto nivel, interpretado y de tipado dinámico.\n"
        "Esto significa que no necesitas declarar el tipo de una variable antes de usarla. A continuación,\n"
        "se describen los tipos de datos básicos más importantes en Python:\n\n"
        "**- Tipos de Datos Numéricos **\n\n"
        "**Enteros (int):**\n"
        "```\na = 5\nb = -3\nc = 0\n```\n"
        "**Números de Punto Flotante (float): **\n"
        "```\nx = 3.14\ny = -0.5\nz = 2.0\n```\n"
        "**Números Complejos (complex):**\n"
        "```\nnum1 = 2 + 3j\nnum2 = -1j\nnum3 = 3.5 + 0j\n```\n"
        "**- Cadenas de Texto (str) **\n"
        "Las cadenas de texto son secuencias de caracteres encerradas entre comillas simples (')\n"
        "o dobles comillas. Las cadenas son inmutables, lo que significa que no se pueden cambiar una vez creadas.\n"
        "```\nsaludo = \"Hola, mundo!\"\nnombre = 'Antonio'\n```\n"
        "**Booleanos (bool) **\n"
        "Los valores booleanos representan verdad (True) o falsedad (False). Son muy útiles\n"
        "en estructuras de control y comparaciones.\n"
        "```\nes_mayor = True\nes_menor = False\n```\n"
        "**Tipos de Datos de Secuencia **\n\n"
        "**Listas (list): **\n"
        "Son colecciones ordenadas y mutables de elementos, que pueden ser de diferentes tipos.\n"
        "```\nnumeros = [1, 2, 3, 4, 5]\nmezcla = [1, 'dos', 3.0, True]\n```\n"
        "**Tuplas (tuple): **\n"
        "Son colecciones ordenadas e inmutables de elementos. Al ser inmutables, son más rápidas y seguras.\n"
        "```\ncoordenadas = (10, 20)\ndatos = ('Antonio', 30, 'España')\n```\n"
        "**Conjuntos (set): **\n"
        "Son colecciones desordenadas de elementos únicos. Son útiles para operaciones\n"
        "de conjunto como uniones e intersecciones.\n"
        "```\nfrutas = {\"manzana\", \"naranja\", \"plátano\"}\n```\n"
        "**Diccionarios (dict): **\n"
        "Son colecciones desordenadas de pares clave-valor. Permiten un acceso rápido a los valores asociados a una clave.\n"
        "```\npersona = {\"nombre\": \"Antonio\", \"edad\": 30, \"ciudad\": \"Madrid\"}\n```\n\n"
        "**Ejemplos de Uso**\n"
        "**Enteros:** \n"
        "a = 10\n"
        "b = -5\n\n"
        "**Flotantes:**\n"
        "pi = 3.14159\n"
        "gravedad = 9.8\n\n"
        "**Complejos:** \n"
        "c = 1 + 2j\n\n"
        "**Cadenas de texto:**\n"
        'saludo = "¡Hola, mundo!"\n'
        "nombre = 'Antonio'\n\n"
        "**Booleanos:**\n"
        "es_adulto = True\n"
        "es_estudiante = False\n\n"
        "**Listas:** \n"
        "numeros = [1, 2, 3, 4, 5]\n"
        "mixtos = [1, \"dos\", 3.0, True]\n\n"
        "**Tuplas:** \n"
        "punto = (10, 20)\n"
        "informacion = (\"Antonio\", 30, \"España\")\n\n"
        "**Conjuntos:**\n"
        "colores = {\"rojo\", \"verde\", \"azul\"}\n\n"
        "**Diccionarios:** \n"
        "coche = {\"marca\": \"Toyota\", \"modelo\": \"Corolla\", \"año\": 2021}\n\n"
        "**Operaciones Básicas**\n\n"
        "**Operaciones Aritméticas:** Suma, resta, multiplicación, división, módulo, y exponenciación.\n"
        "```\nsuma = 10 + 5\nresta = 10 - 5\nmultiplicacion = 10 * 5\ndivision = 10 / 5\nmodulo = 10 % 3\nexponente = 2 ** 3\n```\n"
        "**Operaciones con Listas: **Acceso, modificación, adición y eliminación de elementos.\n"
        "```\ndiccionario = {\"nombre\": \"Antonio\", \"edad\": 30}\ndiccionario[\"edad\"] = 31\ndiccionario[\"ciudad\"] = \"Madrid\"\ndel diccionario[\"edad\"]\n```\n"
    ),
            (
        "enteros",
        "**Ejemplos de enteros (int) en Python**\n\n"
        "**Asignación básica:**\n"
        "```python\n"
        "# Números positivos\n"
        "edad = 25\n"
        "cantidad_productos = 1000\n"
        "año_actual = 2024\n\n"
        "# Números negativos\n"
        "temperatura_bajo_cero = -15\n"
        "deuda = -5000\n\n"
        "# Cero\n"
        "puntos_iniciales = 0\n"
        "```"
        "**Operaciones aritméticas:**\n"
        "```python\n"
        "# Suma\n"
        "resultado_suma = 15 + 10  # 25\n\n"
        "# Resta\n"
        "resultado_resta = 50 - 30  # 20\n\n"
        "# Multiplicación\n"
        "resultado_mult = 7 * 3  # 21\n\n"
        "# División entera (//)\n"
        "resultado_div_entera = 20 // 6  # 3 (descarta decimales)\n\n"
        "# Módulo (%)\n"
        "residuo = 20 % 6  # 2 (resto de la división)\n\n"
        "# Potencia (**)\n"
        "cubo = 3 ** 3  # 27\n\n"
        "```\n"
        "**Uso en contexto real:**\n"
        "```python\n"
        "# Calcular días vividos (aproximado)\n"
        "años = 30\n"
        "días_por_año = 365\n"
        "días_vividos = años * días_por_año  # 10,950\n\n"
        "# Controlar inventario"
        "stock_inicial = 150\n"
        "ventas = 47\n"
        "reposición = 60\n"
        "stock_actual = stock_inicial - ventas + reposición  # 163\n\n"
        "# Conversión de unidades\n"
        "kilómetros = 5\n"
        "metros = kilómetros * 1000  # 5000\n\n"
        "```\n"
        "**Conversión a entero:**\n"
        "```python\n"
        "# Desde string numérico\n"
        'numero_str = "45"\n'
        "numero_int = int(numero_str)  # 45 (ahora es tipo int)\n\n"
        "# Desde float"
        "numero_float = 12.99\n"
        "numero_int = int(numero_float)  # 12 (trunca decimales)\n\n"
        '# Error común (evitar) --> # int("Hola") → ValueError\n'
        "```\n"
        "**Casos especiales:**\n"
        "```python\n"
        "# Notación científica (se almacena como int si no hay decimales)\n"
        "gran_numero = 2e3  # 2000 (tipo int)\n\n"
        "# Sistemas numéricos\n"
        "hexadecimal = 0xFF  # 255 en decimal\n"
        "binario = 0b1010  # 10 en decimal\n"
        "octal = 0o77  # 63 en decimal\n"
        "```\n"
),
            (
        "int",
        "**Ejemplos de enteros (int) en Python**\n\n"
        "**Asignación básica:**\n"
        "```python\n"
        "# Números positivos\n"
        "edad = 25\n"
        "cantidad_productos = 1000\n"
        "año_actual = 2024\n\n"
        "# Números negativos\n"
        "temperatura_bajo_cero = -15\n"
        "deuda = -5000\n\n"
        "# Cero\n"
        "puntos_iniciales = 0\n"
        "```"
        "**Operaciones aritméticas:**\n"
        "```python\n"
        "# Suma\n"
        "resultado_suma = 15 + 10  # 25\n\n"
        "# Resta\n"
        "resultado_resta = 50 - 30  # 20\n\n"
        "# Multiplicación\n"
        "resultado_mult = 7 * 3  # 21\n\n"
        "# División entera (//)\n"
        "resultado_div_entera = 20 // 6  # 3 (descarta decimales)\n\n"
        "# Módulo (%)\n"
        "residuo = 20 % 6  # 2 (resto de la división)\n\n"
        "# Potencia (**)\n"
        "cubo = 3 ** 3  # 27\n\n"
        "```\n"
        "**Uso en contexto real:**\n"
        "```python\n"
        "# Calcular días vividos (aproximado)\n"
        "años = 30\n"
        "días_por_año = 365\n"
        "días_vividos = años * días_por_año  # 10,950\n\n"
        "# Controlar inventario"
        "stock_inicial = 150\n"
        "ventas = 47\n"
        "reposición = 60\n"
        "stock_actual = stock_inicial - ventas + reposición  # 163\n\n"
        "# Conversión de unidades\n"
        "kilómetros = 5\n"
        "metros = kilómetros * 1000  # 5000\n\n"
        "```\n"
        "**Conversión a entero:**\n"
        "```python\n"
        "# Desde string numérico\n"
        'numero_str = "45"\n'
        "numero_int = int(numero_str)  # 45 (ahora es tipo int)\n\n"
        "# Desde float"
        "numero_float = 12.99\n"
        "numero_int = int(numero_float)  # 12 (trunca decimales)\n\n"
        '# Error común (evitar) --> # int("Hola") → ValueError\n'
        "```\n"
        "**Casos especiales:**\n"
        "```python\n"
        "# Notación científica (se almacena como int si no hay decimales)\n"
        "gran_numero = 2e3  # 2000 (tipo int)\n\n"
        "# Sistemas numéricos\n"
        "hexadecimal = 0xFF  # 255 en decimal\n"
        "binario = 0b1010  # 10 en decimal\n"
        "octal = 0o77  # 63 en decimal\n"
        "```\n"
),

            (
        "float",
        "**¿Qué es un float en Python?**\n\n"
        "Los float son números de punto flotante (decimales) que permiten representar valores reales con parte fraccionaria.\n\n"
        "**Ejemplo de uso práctico**\n"
        "```python\n"
        "# 1. Asignación básica\n"
        "temperatura = 23.5\n"       
        "pi = 3.1415926535\n"
        "presupuesto = 1500.75\n\n"
        "# 2. Notación científica\n"
        "velocidad_luz = 3e8      # 300000000.0\n"
        "micro_metro = 1e-6       # 0.000001\n\n"
        "# 3. Operaciones matemáticas\n"
        "radio = 5.0\n"
        "area_circulo = pi * (radio ** 2)  # 78.5398163375\n\n"
        "# 4. Conversiones\n"
        "entero_a_float = float(42)        # 42.0\n"
        'texto_a_float = float("15.75")    # 15.75\n\n'
        "# 5. Resultados de división\n"
        "division = 10 / 3  # 3.3333333333333335 (automáticamente float)\n\n"
        "**Casos especiales**\n"
        "infinito_positivo = float('inf')   # Representa infinito\n"
        "infinito_negativo = -float('inf')  # -infinito\n"
        "no_es_numero = float('nan')        # NaN (Not a Number)\n\n"
        "```\n"
        "**¿Cuándo usar floats?**\n"
        "- Cálculos científicos/ingeniería\n"
        "- Manejo de dinero (aunque mejor usar decimal para precisión absoluta)\n"
        "- Mediciones físicas (peso, temperatura, tiempo)\n"
        "- Gráficos y modelado 3D"
),

            (
        "numeros complejos",
        "**¿Qué es un complex en Python?**\n\n"
        "Los números complejos tienen una parte real y una parte imaginaria (múltiplo de j, la unidad imaginaria).\n\n"
        "**Ejemplo de uso práctico**\n"
        "```python\n"
        "# 1. Asignación directa\n"
        "z1 = 3 + 4j        # Parte real: 3 | Parte imaginaria: 4\n"       
        "z2 = -2.5 - 1.7j   # Números negativos\n"
        "z3 = 0j            # Complejo puramente imaginario (real=0)\n\n"
        "# 2. Usando complex()\n"
        "z4 = complex(2, 5)   # 2 + 5j\n"
        "z5 = complex(1.5)    # 1.5 + 0j (si solo se especifica real)\n\n"
        "```\n"
        "**Operaciones comunes**\n"
        "```python\n"
        "# Suma\n"
        "resultado_suma = (2 + 3j) + (1 - 2j)  # 3 + 1j\n\n"
        "# Multiplicación\n"
        "resultado_mult = (1 + 2j) * (3 - 4j)  # 11 + 2j (3 + 6j -4j -8j² → j²=-1)\n\n"
        '# Conjugado complejo\n'
        "conjugado = (5 - 3j).conjugate()  # 5 + 3j\n\n"
        "# Acceso a partes\n"
        "real = z1.real     # 3.0 (siempre retorna float)\n"
        "imag = z1.imag     # 4.0\n"
        "```\n"

        "**Casos especiales**\n"
        "```python\n"
        "# Desde strings\n"
        'z6 = complex("5+3j")      # 5 + 3j (sin espacios)\n'
        'z7 = complex("2.7")       # 2.7 + 0j\n\n'
        "# Magnitud y fase (módulo y argumento)\n"
        "import cmath\n"
        "modulo = abs(3 + 4j)      # 5.0 (√(3² +4²))\n"
        "fase = cmath.phase(1 + 1j) # 0.785 rad (45°)\n\n"
        "```\n"
        "**Aplicaciones prácticas**\n"
        "```python\n"
        "# 1. Resolver ecuaciones cuadráticas con raíces complejas\n"
        'a, b, c = 1, 2, 5\n'
        "discriminante = b**2 - 4*a*c\n"
        "raiz1 = (-b + cmath.sqrt(discriminante)) / (2*a)  # -1 + 2j\n"
        "raiz2 = (-b - cmath.sqrt(discriminante)) / (2*a)  # -1 - 2j\n\n"
        "# 2. Ingeniería eléctrica (impedancia)\n"
        "resistencia = 4.7  # Ohms (real)\n"
        "reactancia = 3.2j  # Ohms (imaginario)\n"
        "impedancia_total = resistencia + reactancia  # 4.7 + 3.2j\n\n"
        "# 3. Transformadas de Fourier (procesamiento de señales)\n"
        "muestra = [0.5 + 0j, 1j, -0.3 + 0.4j]  # Datos complejos típicos\n\n"
        "```\n"
        "**Precauciones importantes**\n"
        "```python\n"
        "# 1. La 'j' debe ir pegado al número imaginario\n"
        'incorrecto = 3 + j4     # Error (NameError: j4 no existe)\n'
        "correcto = 3 + 4j       # ✓\n\n"
        "# 2. Precisión en representación\n"
        "operacion = (0.1 + 0.2j) * 3  # 0.3 + 0.6j (precisión float)\n\n"
        "```\n"
        "**¿Cuándo usar complex?**\n"
        "- Análisis de circuitos AC\n"
        "- Procesamiento de señales digitales\n"
        "- Mecánica cuántica (funciones de onda)\n"
        "- Gráficos fractales (como el conjunto de Mandelbrot)"
),
            (
        "complex",
        "**¿Qué es un complex en Python?**\n\n"
        "Los números complejos tienen una parte real y una parte imaginaria (múltiplo de j, la unidad imaginaria).\n\n"
        "**Ejemplo de uso práctico**\n"
        "```python\n"
        "# 1. Asignación directa\n"
        "z1 = 3 + 4j        # Parte real: 3 | Parte imaginaria: 4\n"       
        "z2 = -2.5 - 1.7j   # Números negativos\n"
        "z3 = 0j            # Complejo puramente imaginario (real=0)\n\n"
        "# 2. Usando complex()\n"
        "z4 = complex(2, 5)   # 2 + 5j\n"
        "z5 = complex(1.5)    # 1.5 + 0j (si solo se especifica real)\n\n"
        "```\n"
        "**Operaciones comunes**\n"
        "```python\n"
        "# Suma\n"
        "resultado_suma = (2 + 3j) + (1 - 2j)  # 3 + 1j\n\n"
        "# Multiplicación\n"
        "resultado_mult = (1 + 2j) * (3 - 4j)  # 11 + 2j (3 + 6j -4j -8j² → j²=-1)\n\n"
        '# Conjugado complejo\n'
        "conjugado = (5 - 3j).conjugate()  # 5 + 3j\n\n"
        "# Acceso a partes\n"
        "real = z1.real     # 3.0 (siempre retorna float)\n"
        "imag = z1.imag     # 4.0\n"
        "```\n"

        "**Casos especiales**\n"
        "```python\n"
        "# Desde strings\n"
        'z6 = complex("5+3j")      # 5 + 3j (sin espacios)\n'
        'z7 = complex("2.7")       # 2.7 + 0j\n\n'
        "# Magnitud y fase (módulo y argumento)\n"
        "import cmath\n"
        "modulo = abs(3 + 4j)      # 5.0 (√(3² +4²))\n"
        "fase = cmath.phase(1 + 1j) # 0.785 rad (45°)\n\n"
        "```\n"
        "**Aplicaciones prácticas**\n"
        "```python\n"
        "# 1. Resolver ecuaciones cuadráticas con raíces complejas\n"
        'a, b, c = 1, 2, 5\n'
        "discriminante = b**2 - 4*a*c\n"
        "raiz1 = (-b + cmath.sqrt(discriminante)) / (2*a)  # -1 + 2j\n"
        "raiz2 = (-b - cmath.sqrt(discriminante)) / (2*a)  # -1 - 2j\n\n"
        "# 2. Ingeniería eléctrica (impedancia)\n"
        "resistencia = 4.7  # Ohms (real)\n"
        "reactancia = 3.2j  # Ohms (imaginario)\n"
        "impedancia_total = resistencia + reactancia  # 4.7 + 3.2j\n\n"
        "# 3. Transformadas de Fourier (procesamiento de señales)\n"
        "muestra = [0.5 + 0j, 1j, -0.3 + 0.4j]  # Datos complejos típicos\n\n"
        "```\n"
        "**Precauciones importantes**\n"
        "```python\n"
        "# 1. La 'j' debe ir pegado al número imaginario\n"
        'incorrecto = 3 + j4     # Error (NameError: j4 no existe)\n'
        "correcto = 3 + 4j       # ✓\n\n"
        "# 2. Precisión en representación\n"
        "operacion = (0.1 + 0.2j) * 3  # 0.3 + 0.6j (precisión float)\n\n"
        "```\n"
        "**¿Cuándo usar complex?**\n"
        "- Análisis de circuitos AC\n"
        "- Procesamiento de señales digitales\n"
        "- Mecánica cuántica (funciones de onda)\n"
        "- Gráficos fractales (como el conjunto de Mandelbrot)"
),

            (
        "cadena de texto",
        "**¿Qué es una cadena de texto en Python?**\n\n"
        "Las cadenas son secuencias inmutables de caracteres (letras, números, símbolos) encerradas entre comillas.\n\n"
        "**Ejemplo de uso básico**\n"
        "```python\n"
        "# 1. Creación de cadenas\n"
        'saludo = "¡Hola, mundo!"\n'       
        "direccion = 'Calle Falsa 123'\n"
        "poema = '''Roses are red,\n"
        "Violets are blue...'''  # Multilínea\n\n"
        "# 2. Caracteres especiales con escape\n"
        'texto = "Texto con \"comillas\" y \\barra\\"  # Usa \ para escapar\n\n'
        "# 3. Acceso a caracteres\n"
        "primera_letra = saludo[0]  # '¡' (índice 0)\n"
        "ultimo_caracter = saludo[-1]  # '!')\n"
        "subcadena = saludo[1:5]  # 'Hola' (slicing)\n\n"
        "```\n"
        "**Operaciones comunes**\n"
        "```python\n"
        "# Concatenación\n"
        'nombre = "Ana"\n'
        'bienvenida = "Hola, " + nombre + "!"  # "Hola, Ana!"\n\n'
        "# Repetición\n"
        'eco = "ja" * 3  # "jajaja"\n\n'
        "# Formateo con f-strings (Python 3.6+)\n"
        "edad = 25\n"
        'mensaje = f"{nombre} tiene {edad} años"  # "Ana tiene 25 años"\n\n'
        "# Métodos útiles\n"
        'texto = "  Python es Genial  "\n'
        'limpio = texto.strip()  # "Python es Genial" (elimina espacios)\n'
        'mayusculas = texto.upper()  # "  PYTHON ES GENIAL  ")\n'
        'reemplazo = texto.replace("Genial", "Increíble")  # "  Python es Increíble  "\n\n'
        "```\n"
        "**Casos especiales**\n"
        "```python\n"
        "# Unicode y emojis\n"
        'emoji = "Python 🐍"  # Soporta caracteres Unicode\n'
        'hex_code = "\u00A1Hola!"  # ¡Hola! (código hexadecimal)\n\n'
        "# Conversiones\n"
        'numero_str = str(42)  # "42" (entero a cadena)\n'
        'lista = "-".join(["a", "b", "c"])  # "a-b-c" (unión con separador)\n\n'
        "# Comprobaciones\n"
        'es_alfanumerico = "abc123".isalnum()  # True\n'
        'es_digito = "50".isdigit()  # True\n\n'
        "```\n"
        "**Aplicaciones prácticas**\n"
        "```python\n"
        "# 1. Procesamiento de texto\n"
        'frase = "Python es un lenguaje poderoso"\n'
        'palabras = frase.split()  # ["Python", "es", ..., "poderoso"]\n'
        "longitud = len(frase)  # 28 caracteres (incluyendo espacios)\n\n"
        "# 2. Validación de entrada de usuario\n"
        'email = "usuario@dominio.com"\n'
        'if "@" in email and "." in email.split("@")[1]:\n'
        '              print("Email válido")\n\n'
        "# 3. Generación de HTML/XML\n"
        "etiqueta = f'<a href=`{url}`>{texto}</a>'  # Plantillas simples\n\n"
        "# 4. Palíndromos\n"
        'es_palindromo = "anilina" == "anilina"[::-1]  # True (reversa)\n\n'
        "```\n"
        "**Precauciones importantes**\n"
        "```python\n"
        "# 1. Inmutabilidad: No se pueden modificar caracteres individuales\n"
        'cadena = "Hola"\n'
        '# cadena[0] = "M"  # Error: TypeError\n\n'
        "# 2. Codificación de caracteres\n"
        'texto = "Añadir carácter ñ"  # Usar codificación UTF-8 al guardar archivos\n\n'
        "# 3. Performance en concatenaciones grandes\n"
        "# Mejor usar listas y str.join():\n"
        'resultado = "\n".join(partes)  # Eficiente para muchas operaciones\n\n'
        "```\n"
        "**¿Cuándo usar str?**\n"
        "- Manipulación de texto (limpieza, análisis)\n"
        "- Interfaz de usuario y mensajes\n"
        "- Procesamiento de archivos (CSV, JSON, XML)\n"
        "- Generación de contenido dinámico (plantillas web)\n"
        "- Expresiones regulares (búsqueda de patrones)"
),

            (
        "str",
        "**¿Qué es una cadena de texto en Python?**\n\n"
        "Las cadenas son secuencias inmutables de caracteres (letras, números, símbolos) encerradas entre comillas.\n\n"
        "**Ejemplo de uso básico**\n"
        "```python\n"
        "# 1. Creación de cadenas\n"
        'saludo = "¡Hola, mundo!"\n'       
        "direccion = 'Calle Falsa 123'\n"
        "poema = '''Roses are red,\n"
        "Violets are blue...'''  # Multilínea\n\n"
        "# 2. Caracteres especiales con escape\n"
        'texto = "Texto con \"comillas\" y \\barra\\"  # Usa \ para escapar\n\n'
        "# 3. Acceso a caracteres\n"
        "primera_letra = saludo[0]  # '¡' (índice 0)\n"
        "ultimo_caracter = saludo[-1]  # '!')\n"
        "subcadena = saludo[1:5]  # 'Hola' (slicing)\n\n"
        "```\n"
        "**Operaciones comunes**\n"
        "```python\n"
        "# Concatenación\n"
        'nombre = "Ana"\n'
        'bienvenida = "Hola, " + nombre + "!"  # "Hola, Ana!"\n\n'
        "# Repetición\n"
        'eco = "ja" * 3  # "jajaja"\n\n'
        "# Formateo con f-strings (Python 3.6+)\n"
        "edad = 25\n"
        'mensaje = f"{nombre} tiene {edad} años"  # "Ana tiene 25 años"\n\n'
        "# Métodos útiles\n"
        'texto = "  Python es Genial  "\n'
        'limpio = texto.strip()  # "Python es Genial" (elimina espacios)\n'
        'mayusculas = texto.upper()  # "  PYTHON ES GENIAL  ")\n'
        'reemplazo = texto.replace("Genial", "Increíble")  # "  Python es Increíble  "\n\n'
        "```\n"
        "**Casos especiales**\n"
        "```python\n"
        "# Unicode y emojis\n"
        'emoji = "Python 🐍"  # Soporta caracteres Unicode\n'
        'hex_code = "\u00A1Hola!"  # ¡Hola! (código hexadecimal)\n\n'
        "# Conversiones\n"
        'numero_str = str(42)  # "42" (entero a cadena)\n'
        'lista = "-".join(["a", "b", "c"])  # "a-b-c" (unión con separador)\n\n'
        "# Comprobaciones\n"
        'es_alfanumerico = "abc123".isalnum()  # True\n'
        'es_digito = "50".isdigit()  # True\n\n'
        "```\n"
        "**Aplicaciones prácticas**\n"
        "```python\n"
        "# 1. Procesamiento de texto\n"
        'frase = "Python es un lenguaje poderoso"\n'
        'palabras = frase.split()  # ["Python", "es", ..., "poderoso"]\n'
        "longitud = len(frase)  # 28 caracteres (incluyendo espacios)\n\n"
        "# 2. Validación de entrada de usuario\n"
        'email = "usuario@dominio.com"\n'
        'if "@" in email and "." in email.split("@")[1]:\n'
        '              print("Email válido")\n\n'
        "# 3. Generación de HTML/XML\n"
        "etiqueta = f'<a href=`{url}`>{texto}</a>'  # Plantillas simples\n\n"
        "# 4. Palíndromos\n"
        'es_palindromo = "anilina" == "anilina"[::-1]  # True (reversa)\n\n'
        "```\n"
        "**Precauciones importantes**\n"
        "```python\n"
        "# 1. Inmutabilidad: No se pueden modificar caracteres individuales\n"
        'cadena = "Hola"\n'
        '# cadena[0] = "M"  # Error: TypeError\n\n'
        "# 2. Codificación de caracteres\n"
        'texto = "Añadir carácter ñ"  # Usar codificación UTF-8 al guardar archivos\n\n'
        "# 3. Performance en concatenaciones grandes\n"
        "# Mejor usar listas y str.join():\n"
        'resultado = "\n".join(partes)  # Eficiente para muchas operaciones\n\n'
        "```\n"
        "**¿Cuándo usar str?**\n"
        "- Manipulación de texto (limpieza, análisis)\n"
        "- Interfaz de usuario y mensajes\n"
        "- Procesamiento de archivos (CSV, JSON, XML)\n"
        "- Generación de contenido dinámico (plantillas web)\n"
        "- Expresiones regulares (búsqueda de patrones)"
),


    ]

    for prompt, response in prompts_responses:
        add_or_update_predefined_prompt(prompt, response)