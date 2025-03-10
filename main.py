import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame, simpledialog
from PIL import Image, ImageTk
import requests
import json
import threading
import os

# Direct API Key
OPENROUTER_API_KEY = "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"

# Historial de la conversación
conversation_history = []

def chat_with_bot(prompt, update_callback, finish_callback):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})
    
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
                "messages": conversation_history,
                "max_tokens": 750,
                "temperature": 0.5,
                "stream": True  # Habilitar la transmisión de respuestas
            }),
            stream=True
        )
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    decoded_line = decoded_line[6:]
                    if decoded_line != "[DONE]":
                        response_data = json.loads(decoded_line)
                        choice = response_data.get('choices', [{}])[0]
                        message_content = choice.get('delta', {}).get('content', '')
                        update_callback(message_content)
        finish_callback()  # Indicar que el stream ha finalizado
    except Exception as e:
        print(f"Error al llamar a la API de OpenRouter: {e}")
        update_callback("HA HA HA HA no ha dicho la palabra magica.")
        finish_callback()

def on_muneco_double_click(event):
    def send_message(event=None):
        user_text = text_widget.get("1.0", tk.END).strip()
        if user_text:
            response_window = show_response()
            threading.Thread(target=chat_with_bot, args=(user_text, response_window.update_response, response_window.finish_stream)).start()
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

    send_button = Button(frame, text="Enviar", command=send_message, bg='grey', fg='white', font=("Comic Sans MS", 12))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    text_widget = Text(frame, font=("Comic Sans MS", 13), wrap='word', height=1, spacing1=5, spacing3=5,  padx=10)  # Añadir espaciado adicional entre líneas y párrafos
    text_widget.pack(side='left', fill='both', expand=True)
    text_widget.bind("<KeyRelease>", on_text_change)
    text_widget.bind("<Return>", send_message)
    text_widget.bind("<Shift-Return>", lambda event: None)  # Permitir Shift+Enter para nueva línea

    text_widget.focus_set()  # Enfocar automáticamente el campo de entrada

def show_response():
    def copy_to_clipboard(text):
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Actualizar el portapapeles

    class ResponseWindow:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.stream_finished = False
            self.complete_text = ""

        def update_response(self, new_text):
            self.complete_text += new_text
            self.text_widget.insert(tk.END, new_text)
            self.text_widget.yview(tk.END)  # Desplazar la vista hacia el final del texto
            self.text_widget.update_idletasks()

        def finish_stream(self):
            global conversation_history
            conversation_history.append({"role": "bot", "content": self.complete_text})
            self.stream_finished = True
            self.apply_formatting()  # Aplicar formateo una vez finalizado el stream

        def apply_formatting(self):
            self.text_widget.delete("1.0", tk.END)
            if "```" in self.complete_text or "**" in self.complete_text:
                parts = self.complete_text.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        if "**" in part:
                            bold_parts = part.split("**")
                            for j, bold_part in enumerate(bold_parts):
                                if j % 2 == 0:
                                    self.text_widget.insert(tk.END, bold_part)
                                else:
                                    self.text_widget.insert(tk.END, bold_part, "bold")
                        else:
                            self.text_widget.insert(tk.END, part)
                    else:
                        self.insert_code_block(part)
            else:
                self.text_widget.insert(tk.END, self.complete_text)

        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n```java\n", "code")
            self.text_widget.insert(tk.END, text, "code")
            self.text_widget.insert(tk.END, "\n```\n", "code")
            copy_button = Button(self.text_widget, text="Copiar", command=lambda: copy_to_clipboard(text), bg='grey', fg='white', font=("Comic Sans MS", 8))
            self.text_widget.window_create(tk.END, window=copy_button)
            self.text_widget.insert(tk.END, "\n\n")

    response_window = Toplevel(root)
    response_window.title("Respuesta del Chatbot")
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Dimensiones de la ventana de respuesta
    window_width = 800
    window_height = 600
    
    # Calcular la posición para centrar la ventana en la pantalla
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    
    response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    response_window.configure(bg='white')

    frame = Frame(response_window, bg='white')
    frame.pack(expand=True, fill='both')

    # Crear un Frame para encapsular la respuesta con un fondo gris claro
    response_frame = Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
    response_frame.pack(expand=True, fill='both', padx=10, pady=10)

    response_text_widget = Text(response_frame, bg='#ebe8e8', wrap='word', font=("Inter", 14), padx=20, pady=20, spacing1=5, spacing3=5, bd=0)  # Añadir espaciado adicional entre líneas y párrafos
    response_text_widget.tag_configure("code", font=("Courier", 12), background="#f4f4f4", spacing3=10, lmargin1=20, lmargin2=20)  # Añadir margen a la izquierda
    response_text_widget.tag_configure("bold", font=("Times New Roman", 14, "bold"))

    response_text_widget.pack(expand=True, fill='both')

    # Vincular Ctrl+Espacio para copiar el texto
    response_window.bind("<Control-space>", lambda event: copy_to_clipboard(response_text_widget.get("1.0", tk.END)))

    return ResponseWindow(response_text_widget)


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
    def fall_animation(index=1):  # Comenzar con la imagen fall_2
        if index == 1:
            muneco_label.config(image=fall_images[1])
            x = muneco_label.winfo_x()
            y = muneco_label.winfo_y()
            if y < root.winfo_height() - muneco_label.winfo_height():
                muneco_label.place(x=x, y=y+10)
                root.after(50, fall_animation, 1)  # Mantener la imagen fall_2
            else:
                root.after(100, fall_animation, 2)  # Cambiar a la imagen fall_3
        elif index == 2:
            muneco_label.config(image=fall_images[2])
            root.after(100, fall_animation, 0)  # Cambiar a la imagen fall_1
        else:
            muneco_label.config(image=fall_images[0])

    fall_animation()

def move_to_edge(direction):
    def walk_animation(index=0):
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()
        if direction == "left" and x > 0:
            muneco_label.place(x=x-10, y=y)
            root.after(100, walk_animation, index + 1)
        elif direction == "right" and x < root.winfo_width() - muneco_label.winfo_width():
            muneco_label.place(x=x+10, y=y)
            root.after(100, walk_animation, index + 1)

    walk_animation()

def show_animation_menu(event):
    def select_animation(animation):
        if animation == "Gravedad":
            apply_gravity()
        elif animation == "Mover a la izquierda":
            move_to_edge("left")
        elif animation == "Mover a la derecha":
            move_to_edge("right")
        animation_menu.destroy()

    animation_menu = Toplevel(root)
    animation_menu.title("Seleccionar Animación")

    # Obtener la posición del muñeco
    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()

    # Calcular la posición del menú para que aparezca al lado del muñeco
    menu_width = 200
    menu_height = 150
    position_x = x + muneco_label.winfo_width()
    position_y = y

    animation_menu.geometry(f"{menu_width}x{menu_height}+{position_x}+{position_y}")
    animation_menu.configure(bg='white')

    Frame(animation_menu, bg='white').pack(expand=True, fill='both')

    Button(animation_menu, text="Gravedad", command=lambda: select_animation("Gravedad"), bg='grey', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la izquierda", command=lambda: select_animation("Mover a la izquierda"), bg='grey', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la derecha", command=lambda: select_animation("Mover a la derecha"), bg='grey', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)

def on_right_click_release(event):
    show_animation_menu(event)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("ShanksGpt")
root.configure(bg='white')  # Fondo blanco para la ventana

# Configuración para ocupar toda la pantalla
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.attributes("-transparentcolor", "white")
root.attributes("-topmost", True)
root.overrideredirect(True)  # Hacer la ventana sin bordes

# Intentar cargar la fuente "Inter" después de crear la ventana principal
try:
    root.option_add("*Font", "Inter 14")
except Exception as e:
    print(f"Error al cargar la fuente 'Inter': {e}")

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

# Ahora que la ventana principal está creada, cargar las imágenes de animación
fall_images = [ImageTk.PhotoImage(Image.open(f'fall_{i}.png').resize((200, 200), Image.LANCZOS)) for i in range(1, 4)]

# Aplicar gravedad al iniciar la aplicación
root.after(100, apply_gravity)

# Asociar eventos para arrastrar el muñeco y doble clic para el input
muneco_label.bind("<Button-1>", start_move)
muneco_label.bind("<B1-Motion>", do_move)
muneco_label.bind("<Double-1>", on_muneco_double_click)
muneco_label.bind("<ButtonRelease-3>", on_right_click_release)

# Ejecutar el bucle principal de Tkinter
root.mainloop()