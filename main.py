import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame, Label
from PIL import Image, ImageTk
import openai
import os



# Configurar la API key de OpenAI
openai.api_key = "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"


def chat_with_bot(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return "Lo siento, ocurrió un error al intentar comunicarme con el chatbot."

def on_muneco_double_click(event):
    def send_message(event=None):
        user_text = text_widget.get("1.0", tk.END).strip()
        if user_text:
            chatbot_response = chat_with_bot(user_text)
            show_response(chatbot_response)
        input_window.destroy()

    def on_text_change(event):
        content = text_widget.get("1.0", tk.END)
        lines = content.count('\n') + 1
        new_height = min(10, lines)  # Limitar a un máximo de 10 líneas visibles
        text_widget.config(height=new_height)

    input_window = Toplevel(root)
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Dimensiones de la ventana de entrada
    window_width = 600  # Aumentar el ancho
    window_height = 100  # Reducir la altura
    
    # Calcular la posición para centrar la ventana en la parte inferior con un margen
    margin_bottom = 50
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = screen_height - window_height - margin_bottom
    
    input_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    input_window.configure(bg='white')

    frame = Frame(input_window, bg='white')
    frame.pack(pady=10, padx=10, expand=True, fill='both')

    send_button = Button(frame, text="Enviar", command=send_message, bg='blue', fg='white', font=("Arial", 14))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    text_widget = Text(frame, font=("Arial", 14), wrap='word', height=1)
    text_widget.pack(side='left', fill='both', expand=True)
    text_widget.bind("<KeyRelease>", on_text_change)
    text_widget.bind("<Return>", send_message)
    text_widget.bind("<Shift-Return>", lambda event: None)  # Permitir Shift+Enter para nueva línea

    text_widget.focus_set()  # Enfocar automáticamente el campo de entrada

def show_response(response_text):
    response_window = Toplevel(root)
    response_window.title("Respuesta del Chatbot")
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Dimensiones de la ventana de respuesta
    window_width = 400
    window_height = 200
    
    # Calcular la posición para centrar la ventana en la pantalla
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    
    response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    response_window.configure(bg='white')

    response_label = Label(response_window, text=response_text, bg='white', wraplength=350, font=("Arial", 14), justify="center")
    response_label.pack(pady=20, padx=20, expand=True, fill='both')

    close_button = Button(response_window, text="Cerrar", command=response_window.destroy, bg='red', fg='white', font=("Arial", 14))
    close_button.pack(pady=10)

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
root.configure(bg='white')  # Fondo blanco para la ventana

# Configuración para ocupar toda la pantalla
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)
root.overrideredirect(True)  # Hacer la ventana sin bordes

# Crear un canvas
canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Cargar el muñeco y redimensionarlo
try:
    muneco_image = Image.open('C:/Users/RuXx/Documents/Selina_IA/muneco.png')
    muneco_image = muneco_image.resize((200, 200), Image.LANCZOS)  # Redimensionar la imagen
    muneco_photo = ImageTk.PhotoImage(muneco_image)
except Exception as e:
    print(f"Error al cargar la imagen: {e}")
    root.destroy()
    exit()

# Crear un label para el muñeco y colocar en el canvas
muneco_label = tk.Label(root, image=muneco_photo, bg='white')
muneco_label.place(x=200, y=100)  # Colocar el muñeco en el centro de la ventana

# Asociar eventos para arrastrar el muñeco y doble clic para el input
muneco_label.bind("<Button-1>", start_move)
muneco_label.bind("<B1-Motion>", do_move)
muneco_label.bind("<Double-1>", on_muneco_double_click)

# Crear un label para mostrar la respuesta del chatbot
response_label = tk.Label(root, text="", bg='grey', wraplength=400, font=("Arial", 14), justify="center")
response_label.place(relx=0.5, rely=0.75, anchor='center')

# Ejecutar el bucle principal de Tkinter
root.mainloop()