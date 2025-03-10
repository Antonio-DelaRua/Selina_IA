import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame, simpledialog
from PIL import Image, ImageTk
import requests
import json

# Direct API Key
OPENROUTER_API_KEY = "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"

def chat_with_bot(prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Opcional. URL del sitio para rankings en openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>",  # Opcional. Título del sitio para rankings en openrouter.ai.
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.5,
            })
        )
        response_data = response.json()
        return response_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error al llamar a la API de OpenRouter: {e}")
        return "HA HA HA HA no ha dicho la palabra magica."

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

    send_button = Button(frame, text="Enviar", command=send_message, bg='blue', fg='white', font=("Comic Sans MS", 12))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    text_widget = Text(frame, font=("Times New Roman", 14), wrap='word', height=1)
    text_widget.pack(side='left', fill='both', expand=True)
    text_widget.bind("<KeyRelease>", on_text_change)
    text_widget.bind("<Return>", send_message)
    text_widget.bind("<Shift-Return>", lambda event: None)  # Permitir Shift+Enter para nueva línea

    text_widget.focus_set()  # Enfocar automáticamente el campo de entrada

def show_response(response_text):
    def copy_to_clipboard(event=None):
        response_text_widget.config(state=tk.NORMAL)
        root.clipboard_clear()
        root.clipboard_append(response_text_widget.get("1.0", tk.END))
        response_text_widget.config(state=tk.DISABLED)

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

    frame = Frame(response_window, bg='white')
    frame.pack(expand=True, fill='both')

    response_text_widget = Text(frame, bg='white', wrap='word', font=("Times New Roman", 14), padx=20, pady=20)
    response_text_widget.insert(tk.END, response_text)
    response_text_widget.config(state=tk.DISABLED)  # Hacer el widget de texto de solo lectura
    response_text_widget.pack(expand=True, fill='both')

    # Vincular Ctrl+Espacio para copiar el texto
    response_window.bind("<Control-space>", copy_to_clipboard)

def reset_api_key(event=None):
    global OPENROUTER_API_KEY
    OPENROUTER_API_KEY = simpledialog.askstring("API Key", "Por favor, introduce tu clave de API de OpenRouter:")

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

def apply_gravity():
    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()
    if y < root.winfo_height() - muneco_label.winfo_height():
        muneco_label.place(x=x, y=y+10)
        root.after(50, apply_gravity)  # Aplicar gravedad cada 50 ms

def on_right_click_release(event):
    apply_gravity()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("ShanksGpt")
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

# Obtener las dimensiones de la pantalla y calcular la posición inicial del muñeco
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
initial_x = (screen_width // 2) - (200 // 2)
initial_y = (screen_height // 2) - (200 // 2)

# Colocar el muñeco en el centro de la ventana
muneco_label.place(x=initial_x, y=initial_y)

# Aplicar gravedad al iniciar la aplicación
root.after(100, apply_gravity)

# Asociar eventos para arrastrar el muñeco y doble clic para el input
muneco_label.bind("<Button-1>", start_move)
muneco_label.bind("<B1-Motion>", do_move)
muneco_label.bind("<Double-1>", on_muneco_double_click)
muneco_label.bind("<ButtonRelease-3>", on_right_click_release)

# Vincular Ctrl+1 para restablecer la clave de API
root.bind("<Control-Key-1>", reset_api_key)

# Ejecutar el bucle principal de Tkinter
root.mainloop()