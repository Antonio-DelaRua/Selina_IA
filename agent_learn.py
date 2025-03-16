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

        
    ]

    for prompt, response in prompts_responses:
        add_or_update_predefined_prompt(prompt, response)