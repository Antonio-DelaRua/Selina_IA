def formatear_texto(texto):
    lineas = texto.split('\n')
    lineas_con_comillas = [f'"{linea.strip()}\\n"' for linea in lineas if linea.strip()]
    resultado = "```\n" + "\n".join(lineas_con_comillas) + "\n```"
    return resultado

# Usar una de estas opciones al abrir el archivo:
try:
    # Opción 1 (recomendada):
    with open("plantilla.txt", "r", encoding='utf-8') as f:
        texto = f.read()
    
    # Opción 2 (si falla utf-8):
    # with open("input.txt", "r", encoding='latin-1') as f:
    #     texto = f.read()

except UnicodeDecodeError:
    print("Error: El archivo tiene una codificación no compatible.")
    texto = ""

texto_formateado = formatear_texto(texto)
print(texto_formateado)