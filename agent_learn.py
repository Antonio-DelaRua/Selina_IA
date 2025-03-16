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
        ("¿Qué es SQL?", "SQL es un lenguaje de programación utilizado para gestionar y manipular bases de datos relacionales."),
        ("¿Qué es NoSQL?", "NoSQL es un enfoque de diseño de base de datos que proporciona un mecanismo para el almacenamiento y recuperación de datos, que está modelado de formas distintas a las tablas relacionales."),
        # Agrega más pares de prompt y response aquí
        ("me cuentas un chiste?", "Doctor me tiemblan muchos las manos. -¿no sera que bebe demasiado alcohol? - que va si lo tiro casi todo"),

        
    ]

    for prompt, response in prompts_responses:
        add_or_update_predefined_prompt(prompt, response)