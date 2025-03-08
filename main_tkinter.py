import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import openai

# Configurar la API key de OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"

def chat_with_bot(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return "Lo siento, ocurrió un error al intentar comunicarme con el chatbot."

def on_muneco_double_click(event):
    user_text = simpledialog.askstring("Input", "¿Qué quieres decir?", parent=root)
    if user_text:
        chatbot_response = chat_with_bot(user_text)
        response_label.config(text=chatbot_response)

def start_move(event):
    global startX, startY
    startX = event.x
    startY = event.y

def do_move(event):
    x = muneco_label.winfo_x() + event.x - startX
    y = muneco_label.winfo_y() + event.y - startY

    # Limitar el movimiento dentro de los límites de la ventana
    if x < 0:
        x = 0
    elif x > root.winfo_width() - muneco_label.winfo_width():
        x = root.winfo_width() - muneco_label.winfo_width()

    if y < 0:
        y = 0
    elif y > root.winfo_height() - muneco_label.winfo_height():
        y = root.winfo_height() - muneco_label.winfo_height()

    muneco_label.place(x=x, y=y)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Muñeco Interactivo")
root.geometry("800x600")
root.configure(bg='white')  # Fondo blanco para la ventana
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)

# Crear un canvas
canvas = tk.Canvas(root, width=800, height=600, bg='white', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Cargar el muñeco
muneco_image = Image.open('C:/Users/RuXx/Documents/SelinaIA/muneco.png')
muneco_photo = ImageTk.PhotoImage(muneco_image)

# Crear un label para el muñeco y colocar en el canvas
muneco_label = tk.Label(root, image=muneco_photo, bg='white')
muneco_label.place(x=400, y=300)  # Colocar el muñeco en el centro de la ventana

# Asociar eventos para arrastrar el muñeco y doble clic para el input
muneco_label.bind("<Button-1>", start_move)
muneco_label.bind("<B1-Motion>", do_move)
muneco_label.bind("<Double-1>", on_muneco_double_click)

# Crear un label para mostrar la respuesta del chatbot
response_label = tk.Label(root, text="", bg='grey', wraplength=400, font=("Arial", 14), justify="center")
response_label.place(relx=0.5, rely=0.75, anchor='center')

# Ejecutar el bucle principal de Tkinter
root.mainloop()