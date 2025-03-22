import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame
from PIL import Image, ImageTk
import threading
from agent import agent
from movimientos import apply_gravity, move_to_edge, climb_animation
import re
import speech_recognition as sr

# Variables globales para la ventana de respuesta
response_window = None
response_text_widget = None


# Función para manejar el doble clic en el muñeco
def on_muneco_double_click(event, root):
    input_window = tk.Toplevel(root)

    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Dimensiones de la ventana de entrada
    window_width = 600
    window_height = 80

    # Calcular la posición para centrar la ventana en la parte inferior con un margen
    margin_bottom = 50
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = screen_height - window_height - margin_bottom

    input_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    input_window.configure(bg='white')

    frame = tk.Frame(input_window, bg='white')
    frame.pack(pady=10, padx=10, expand=True, fill='both')

    # Botón de micrófono
    mic_button = tk.Button(frame, text="🎤", 
                     command=lambda: start_listening_thread(text_widget, root, input_window),
                     bg='orange', fg='white', font=("Comic Sans MS", 12))
    mic_button.pack(side='left', padx=10, pady=10, fill='y')

    # Animación de pulso al grabar
    def pulse_mic():
        current_color = mic_button.cget("background")
        new_color = '#ff4500' if current_color == 'orange' else 'orange'
        mic_button.config(background=new_color)
        if text_widget.tag_ranges("recording"):  # Si sigue grabando
            root.after(500, pulse_mic)
    
    mic_button.config(command=lambda: [
        start_listening_thread(text_widget, root, input_window),
        pulse_mic()
    ])

    # Botón de enviar
    send_button = tk.Button(frame, text="Enviar", command=lambda: send_message(input_window, root, text_widget), 
                          bg='orange', fg='white', font=("Comic Sans MS", 12))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    text_widget = tk.Text(frame, font=("Comic Sans MS", 13), wrap='word', height=1, spacing1=5, spacing3=5, padx=10, highlightthickness=0, bd=1, relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)
    text_widget.bind("<KeyRelease>", lambda event: on_text_change(event, text_widget))
    text_widget.bind("<Return>", lambda event: send_message(input_window, root, text_widget))
    text_widget.bind("<Shift-Return>", lambda event: None)
    text_widget.bind("<Control-m>", lambda event: start_listening_thread(text_widget, root))

    text_widget.focus_set()



# Función para iniciar el hilo de escucha
def start_listening_thread(text_widget, root, input_window):  # Añadir input_window como parámetro
    threading.Thread(target=listen_and_convert, 
                   args=(text_widget, root, input_window)).start()  # Pasar input_window


# Función para escuchar y convertir voz a texto
def listen_and_convert(text_widget, root, input_window):
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            # Actualizar la interfaz
            root.after(0, text_widget.delete, "1.0", tk.END)
            root.after(0, text_widget.insert, tk.END, "Escuchando...")
            text_widget.update_idletasks()
            
            # Configurar para reducir ruido ambiental
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10)
            
            # Convertir audio a texto
            text = recognizer.recognize_google(audio, language='es-ES')
            
            # Actualizar el cuadro de texto
            root.after(0, text_widget.delete, "1.0", tk.END)
            root.after(0, text_widget.insert, "1.0", text)
            # Enviar automáticamente después de 0.5 segundos
            root.after(500, lambda: send_message(input_window, root, text_widget))
            
    except sr.WaitTimeoutError:
        show_error_message(root, "Tiempo de espera agotado", input_window)
    except sr.UnknownValueError:
        show_error_message(root, "Tiempo de espera agotado", input_window)
    except sr.RequestError as e:
        show_error_message(root, f"Error en el servicio: {e}", input_window)
    except Exception as e:
        show_error_message(root, f"Error inesperado: {str(e)}", input_window)


# Función para mostrar mensajes de error
def show_error_message(root, message, input_window):
    response_window = show_response(root)
    response_window.update_response(f"❌ : {message}")
        # Verifica si input_window existe antes de cerrarlo
    if input_window and input_window.winfo_exists():
        input_window.destroy()
    



# Función para enviar mensajes
def send_message(input_window, root, text_widget):
    user_text = text_widget.get("1.0", tk.END).strip()
    if user_text:
        response_window_instance = show_response(root)
        response_window_instance.update_response("Consultando...")  # Mostrar mensaje de espera

        # Usar el agente para obtener una respuesta en un hilo separado
        threading.Thread(target=fetch_response, args=(user_text, response_window_instance)).start()
    input_window.destroy()


# Función para obtener la respuesta del agente
def fetch_response(user_text, response_window_instance):
    # response = agent(user_text)  # Asegúrate de que 'agent' está definido y funciona correctamente
    # Simulación de respuesta del agente (para pruebas)
    response = agent(user_text)
    if response is None:
        response = "Lo siento, no pude obtener una respuesta en este momento."
    response_window_instance.update_response(response)


# Función para ajustar la altura del cuadro de texto
def on_text_change(event, text_widget):
    content = text_widget.get("1.0", tk.END)
    lines = content.count('\n') + 1
    new_height = min(10, lines)  # Limitar a un máximo de 10 líneas visibles
    text_widget.config(height=new_height)



# Función para mostrar la ventana de respuesta
def show_response(root):
    global response_window, response_text_widget

    def copy_to_clipboard(text):
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

    class ResponseWindow:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.complete_text = ""

        def update_response(self, new_text):
            if "Consultando..." in self.complete_text:
                self.complete_text = self.complete_text.replace("Consultando...", "")
            self.complete_text += new_text
            self.text_widget.delete("1.0", tk.END)
            self.insert_formatted_text(self.complete_text)
            self.text_widget.yview(tk.END)
            self.text_widget.update_idletasks()
            self.text_widget.see("1.0")

        def insert_formatted_text(self, text):
            self.text_widget.delete("1.0", tk.END)
            lines = text.split('\n')
            in_code_block = False
            code_block_text = ""

            for line in lines:
                if line.startswith("```"):
                    if in_code_block:
                        self.insert_code_block(code_block_text)
                        in_code_block = False
                        code_block_text = ""
                    else:
                        in_code_block = True
                elif in_code_block:
                    code_block_text += line + "\n"
                else:
                    # Expresión regular para dividir por negrita, cursiva y código en línea
                    parts = re.split(r'(`[^`]+`|\*\*.*?\*\*|\*.*?\*)', line)

                    formatos = {
                        "# ": ("h1md", 1),
                        "## ": ("h2md", 2),
                        "### ": ("h3md", 3)
                    }

                    for part in parts:
                        if isinstance(part, str) and part:
                            if part.startswith("`") and part.endswith("`") and len(part) > 2:
                                # Si está dentro de backticks, aplicamos el estilo "inline_code"
                                self.text_widget.insert(tk.END, part[1:-1], "comillas_simples")
                            else:
                                header_processed = False
                                for prefijo, (tag, longitud) in formatos.items():
                                    if part.startswith(prefijo):
                                        self.text_widget.insert(tk.END, part[longitud:].strip(), tag)
                                        header_processed = True
                                        break
                                if not header_processed:
                                    if part.startswith("*") and part.endswith("*") and len(part) > 2 and part.count("*") == 2:
                                        self.text_widget.insert(tk.END, part[1:-1].strip(), "italic")
                                    elif part.startswith("**") and part.endswith("**") and len(part) > 4 and part.count("*") == 4:
                                        self.text_widget.insert(tk.END, part[2:-2], "negrita")
                                    else:
                                        self.text_widget.insert(tk.END, part)

                    # Agregar un solo salto de línea al final de cada línea
                    self.text_widget.insert(tk.END, "\n")

                    
        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n", "code")
            self.text_widget.insert(tk.END, text, "code")
            self.text_widget.insert(tk.END, "\n", "code")
            code_start = self.text_widget.index(tk.END)
            self.text_widget.insert(tk.END, "\n\n")


            
            button_frame = tk.Frame(self.text_widget, bg="#f4f4f4")
            
            def copy_code():
                self.text_widget.clipboard_clear()
                self.text_widget.clipboard_append(text.strip())
                
            copy_button = tk.Button(
                button_frame, 
                text="Copiar código",
                command=copy_code,
                bg='grey', 
                fg='white', 
                font=("Courier", 10, "bold")
            )
            copy_button.pack(pady=0)
            self.text_widget.window_create(code_start, window=button_frame)

    if response_window is None or not response_window.winfo_exists():
        response_window = tk.Toplevel(root)
        response_window.title("NoBt GPT  \U0001F4BB")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        response_window.configure(bg='white')
        response_window.attributes("-topmost", True)

        frame = tk.Frame(response_window, bg='white')
        frame.pack(expand=True, fill='both')

        response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
        response_frame.pack(expand=True, fill='both', padx=20, pady=20)

        response_text_widget = tk.Text(response_frame, bg='#ebe8e8', wrap='word', font=("Inter", 14), padx=20, pady=20, 
                                      spacing1=10, spacing2=12, spacing3=15, bd=0)
        
        
        # Configure tags on the actual Text widget

        # Estilo formateado del codigo (``` ```)
        response_text_widget.tag_configure("code", 
                font=("Courier", 12, "bold"), 
                background="#f4f4f4",
                lmargin1=30,   # 30 píxeles de margen izquierdo
                lmargin2=10,   # 30 píxeles para líneas que se parten
                rmargin=30     # 30 píxeles de margen derecho
            )
            
        # Estilo para encabezado 1 (#)
        response_text_widget.tag_configure("h1md",
            font=("Segoe UI", 24, "bold"),
            foreground="#1a1a1a",
            spacing1=0,
            spacing3=0,
            lmargin1=0,
            lmargin2=0,
            
        )

        # Estilo para encabezado 2 (##)
        response_text_widget.tag_configure("h2md",
            font=("Helvetica", 20, "bold"),
            foreground="#3a3a3a",
            spacing1=20,
            spacing3=12,
            underline=True,
            justify="left"
        )

        # Estilo para encabezado 3 (###)
        response_text_widget.tag_configure("h3md",
            font=("Segoe UI", 18, "bold"),
            foreground="#3a3a3a",

        )

        # Estilo para cursiva (*texto*)
        response_text_widget.tag_configure("italic",
            font=("Segoe UI", 12, "italic"),
            foreground="#444444"
        )

        # Estilo para negrita (**texto**)
        response_text_widget.tag_configure("negrita",
            font=("Times New Roman", 16, "bold")
        )

        # Estilo para comillas simples (`texto`)
        response_text_widget.tag_configure("comillas_simples",
                                    font=("Courier", 15, "bold"),
                                    foreground="orange"  
        )

        response_text_widget.pack(expand=True, fill='both')

        response_window.bind("<Control-space>", lambda event: copy_to_clipboard(response_text_widget.get("1.0", tk.END)))

    return ResponseWindow(response_text_widget)



# Funciones para el movimiento del muñeco
def start_move(event):
    global startX, startY
    startX = event.x
    startY = event.y

def do_move(event, muneco_label, root):
    x = muneco_label.winfo_x() + event.x - startX
    y = muneco_label.winfo_y() + event.y - startY

    # Usar dimensiones del escritorio virtual
    virtual_width = root.winfo_vrootwidth()
    virtual_height = root.winfo_vrootheight()

    if x < 0:
        x = 0
    elif x > virtual_width - muneco_label.winfo_width():
        x = virtual_width - muneco_label.winfo_width()

    if y < 0:
        y = 0
    elif y > virtual_height - muneco_label.winfo_height():
        y = virtual_height - muneco_label.winfo_height()

    muneco_label.place(x=x, y=y)


def show_animation_menu(event, root, muneco_label, fall_images, walk_images, climb_images, fly_image, muneco_photo):
    def select_animation(animation):
        global animacion_id  # Usamos una variable global para rastrear la animación activa

        # Si hay una animación en curso, la cancelamos
        if "animacion_id" in globals() and animacion_id:
            root.after_cancel(animacion_id)

        # Ejecutamos la animación seleccionada
        if animation == "Gravedad":
            animacion_id = apply_gravity(muneco_label, root, fall_images, muneco_photo)
        elif animation == "Mover a la izquierda":
            animacion_id = move_to_edge("left", muneco_label, root, walk_images, muneco_photo)
        elif animation == "Mover a la derecha":
            animacion_id = move_to_edge("right", muneco_label, root, walk_images, muneco_photo)
        elif animation == "Escalar":
            animacion_id = climb_animation(muneco_label, root, climb_images, fly_image, muneco_photo)

        animation_menu.destroy()

    animation_menu = Toplevel(root)
    animation_menu.title("Seleccionar Animación")

    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()
    menu_width = 200
    menu_height = 240
    position_x = x + muneco_label.winfo_width()
    position_y = y

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    if position_x + menu_width > screen_width:
        position_x = x - menu_width
    if position_x < 0:
        position_x = x + muneco_label.winfo_width()
    if position_y + menu_height > screen_height:
        position_y = screen_height - menu_height - 10

    animation_menu.geometry(f"{menu_width}x{menu_height}+{position_x}+{position_y}")
    animation_menu.configure(bg='white')

    Frame(animation_menu, bg='white').pack(expand=True, fill='both')

    Button(animation_menu, text="Gravedad", command=lambda: select_animation("Gravedad"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la izquierda", command=lambda: select_animation("Mover a la izquierda"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la derecha", command=lambda: select_animation("Mover a la derecha"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Escalar", command=lambda: select_animation("Escalar"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)

# Función para cargar imágenes
def load_images():
    image_paths = {
        "muneco": "img/muneco.png",
        "fall": ["img/fall_1.png", "img/fall_2.png", "img/fall_3.png"],
        "walk_left": ["img/walk_left_1.png", "img/walk_left_2.png" , "img/walk_left_3.png"],
        "climb": ["img/climb_1.png", "img/climb_2.png", "img/climb_3.png"],
        "fly": "img/volar.png"
    }

    images = {}

    for key, paths in image_paths.items():
        if isinstance(paths, list):
            images[key] = [ImageTk.PhotoImage(Image.open(path).resize((200, 200), Image.LANCZOS)) for path in paths]
        else:
            images[key] = ImageTk.PhotoImage(Image.open(paths).resize((200, 200), Image.LANCZOS))

    return images


# Función para configurar la interfaz gráfica
def setup_gui(root):
    root.title("NoBt GPT  \U0001F40D")
    root.configure(bg='white')

    # Obtener dimensiones del escritorio virtual (todas las pantallas)
    virtual_width = root.winfo_vrootwidth()
    virtual_height = root.winfo_vrootheight()
    root.geometry(f"{virtual_width}x{virtual_height}+0+0")  # Cubrir todas las pantallas
    root.attributes("-transparentcolor", "white")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    try:
        root.option_add("*Font", "Inter 14")
    except Exception as e:
        print(f"Error al cargar la fuente 'Inter': {e}")

    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    images = load_images()
    muneco_photo = images["muneco"]
    fall_images = images["fall"]
    walk_images = images["walk_left"]
    climb_images = images["climb"]
    fly_image = images["fly"]

    muneco_label = tk.Label(root, image=muneco_photo, bg='white')
    muneco_label.current_after_id = None  # Nuevo atributo para controlar las animaciones

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    initial_x = (screen_width // 2) - (200 // 2)
    initial_y = (screen_height // 2) - (200 // 2)
    muneco_label.place(x=initial_x, y=initial_y)


    root.after(100, apply_gravity, muneco_label, root, fall_images, muneco_photo)

    muneco_label.bind("<Button-1>", start_move)
    muneco_label.bind("<B1-Motion>", lambda event: do_move(event, muneco_label, root))
    muneco_label.bind("<Double-1>", lambda event: on_muneco_double_click(event, root))
    muneco_label.bind("<ButtonRelease-3>", lambda event: show_animation_menu(event, root, muneco_label, fall_images, walk_images, climb_images, fly_image, muneco_photo))
    
    # Bind Ctrl+Q to close the application
    root.bind("<Control-q>", lambda event: [print("Bye Bye Camarada"), root.destroy()])
    

    return muneco_label, images

if __name__ == "__main__":
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()