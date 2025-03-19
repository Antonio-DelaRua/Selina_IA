def format_markdown(md_text):
    """
    Formatea texto Markdown detectando saltos de párrafo lógicos y añadiendo \n\n.
    """
    lines = md_text.split("\n")
    formatted_lines = []

    for i, line in enumerate(lines):
        # Elimina espacios en blanco al principio y al final de la línea
        stripped_line = line.strip()

        # Si la línea no está vacía y la anterior tampoco, y la actual no empieza con "```" (bloque de código), añade \n\n
        if i > 0 and stripped_line and lines[i-1].strip() and not stripped_line.startswith("```"):
            formatted_lines[-1] = formatted_lines[-1].replace("\\n", "\\n\\n") # Reemplaza el anterior \n por \n\n
        
        formatted_lines.append(f'"{line}\\n"')

    formatted_text = "\n".join(formatted_lines)
    
    with open("formatted_output.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)
    
    print("Archivo formateado generado: formatted_output.txt")


# Ejemplo de entrada Markdown (tu contenido)
md_content = """



"""


format_markdown(md_content)