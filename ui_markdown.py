from tkintermd.frame import TkintermdFrame
from tkinterweb import HtmlFrame
import markdown
import tempfile

import tkinter as tk
from tkinter.constants import *


mkdown="""
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

## 🔗 Enlaces e Imágenes

[OpenAI](https://openai.com)

![Imagen de Ejemplo](https://via.placeholder.com/150)

## 📌 Citas y Separadores

> "El conocimiento es poder." — Francis Bacon

---

## ✅ Checklists

- [x] Aprender Markdown
- [ ] Aplicarlo en mis proyectos
- [ ] Compartirlo con el mundo 🌍

¡Espero que te sirva! 🚀


"""
m_html = markdown.markdown(mkdown)
root = tk.Tk()
frame = HtmlFrame(root, messages_enabled=False)


# load the HTML template with css styles
style =  open("template.html").read()

# create a temporary file to save the HTML content
temp_html = tempfile.NamedTemporaryFile(mode='w')

body_start = '<body>'
body_end = '</body>'

# write the HTML content to the temporary file adding the markdown content and css styles
f = open(temp_html.name, 'w')
f.write(style + body_start+ m_html.replace("```","") + body_end)
f.flush()
frame.load_file(f.name)
frame.pack(fill="both", expand=True)
root.mainloop()
