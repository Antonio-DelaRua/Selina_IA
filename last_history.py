import os
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

HISTORIAL_FILE = "historial_respuestas.txt"

def guardar_en_txt(prompt, response, max_entries=10):
    """
    Guarda la consulta y la respuesta en un archivo de texto, manteniendo solo las últimas 10 entradas.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_entrada = f"\n\n{'=' * 100}\n📅 Fecha: {timestamp}\n❓ Pregunta: {prompt}\n💡 Respuesta:\n{response}\n{'=' * 100}\n\n"

    # Leer historial existente
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = f.read().strip().split("=" * 100 + "\n\n")  # Separar correctamente

        historial = (historial[-(max_entries - 1):] if len(historial) >= max_entries else historial) + [nueva_entrada]
    else:
        historial = [nueva_entrada]

    # Sobrescribir el archivo con las últimas entradas
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(historial) + "\n")

def mostrar_historial():
    """
    Muestra el historial en la ventana Tkinter.
    """
    if not os.path.exists(HISTORIAL_FILE):
        historial_text.set("⚠️ No hay historial guardado aún.")
        return
    
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        historial = f.read()
    
    # Mostrar en el Text widget
    text_widget.config(state="normal")  # Habilitar edición temporal
    text_widget.delete(1.0, tk.END)  # Limpiar contenido anterior
    text_widget.insert(tk.END, historial)  # Insertar historial
    text_widget.config(state="disabled")  # Bloquear edición

# Crear la ventana principal
root = tk.Tk()
root.title("Asistente - Preguntas y Respuestas")

# Crear un widget de texto con desplazamiento
text_widget = scrolledtext.ScrolledText(root, width=100, height=30, wrap=tk.WORD)
text_widget.pack(padx=10, pady=10)
text_widget.config(state="disabled")  # Solo lectura

# Botón para cargar el historial
boton_cargar = tk.Button(root, text="Mostrar Historial", command=mostrar_historial)
boton_cargar.pack(pady=5)

# Variable para mensajes de historial vacío
historial_text = tk.StringVar()

# Ejecutar la aplicación
root.mainloop()
