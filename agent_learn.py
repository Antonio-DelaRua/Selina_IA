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

    ]

    for prompt, response in prompts_responses:
        add_or_update_predefined_prompt(prompt, response)