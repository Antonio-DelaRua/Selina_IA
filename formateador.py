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
# 🌟 Guía Rápida de Markdown

Markdown es un lenguaje de marcado ligero que permite dar formato a texto de forma sencilla. Es muy útil para documentaciones, blogs y notas. ¡Vamos a verlo en acción!

## 📝 Encabezados

Puedes usar `#` para crear encabezados:

```markdown
# Encabezado 1
## Encabezado 2
### Encabezado 3
```

## 📋 Listas

### Lista Ordenada:

1. Primer elemento
2. Segundo elemento
3. Tercer elemento

### Lista No Ordenada:

- Elemento A
- Elemento B
  - Sub-elemento B1
  - Sub-elemento B2
- Elemento C

## 💡 Énfasis y Código

Puedes resaltar texto de varias formas:

- **Negrita** con `**negrita**`
- *Cursiva* con `*cursiva*`
- ~~Tachado~~ con `~~tachado~~`

Bloques de código:

```python
# Esto es un código en Python
def hola_mundo():
    print("¡Hola, mundo!")
```

Código en línea: `console.log("Hola mundo");`

## 📠 Enlaces e Imágenes

[OpenAI](https://openai.com)

## 📌 Citas y Separadores

> "El conocimiento es poder." — Francis Bacon

---

## ✅ Checklists

- [x] Aprender Markdown
- [ ] Aplicarlo en mis proyectos
- [ ] Compartirlo con el mundo 🌍

¡Espero que te sirva! 🚀

"""


format_markdown(md_content)
