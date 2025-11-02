import re

texto_original = """(
    "que es python?",
    "*Python*  es un lenguaje de programación de alto nivel, interpretado y de propósito general."
    "Es conocido por su sintaxis sencilla y legible, lo que facilita su aprendizaje y uso.\n"
    "## ¿Para qué se utiliza Python?\n\n"
    "Python es muy versátil y se usa en diversos campos, como:\n\n"
    "- **Desarrollo web**: Con frameworks como Django y Flask.\n"
    "- **Ciencia de datos y Machine Learning**: Con bibliotecas como NumPy, Pandas, TensorFlow y Scikit-learn.\n"
    "- **Automatización y scripting**: Para escribir scripts que automatizan tareas repetitivas.\n"
    "- **Ciberseguridad**: Para análisis forense y pruebas de penetración.\n"
    "- **Desarrollo de videojuegos**: Con motores como Pygame.\n"
    "- **Administración de sistemas**: Para gestionar servidores y redes.\n"
    "- **Aplicaciones de escritorio**: Usando Tkinter o PyQt.\n"
    "- **Internet de las Cosas (IoT)**: Para programar dispositivos inteligentes."
),"""

def limpiar_comillas(texto):
    lineas = texto.split('\n')
    resultado = []
    
    for linea in lineas:
        # Elimina comillas iniciales/finales y comas residuales
        linea_limpia = re.sub(
            r'^\s*"(?=\S)(.*?)(?<=\S)"\s*,?\s*$', 
            lambda m: m.group(1).strip(), 
            linea
        )
        resultado.append(linea_limpia)
    
    return '\n'.join(resultado)

texto_limpio = limpiar_comillas(texto_original)

with open('limpio.txt', 'w', encoding='utf-8') as f:
    f.write(texto_limpio)