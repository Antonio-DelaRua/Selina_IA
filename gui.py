
import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame
from PIL import Image, ImageTk
from agent import agent
from movimientos import apply_gravity, move_to_edge, climb_animation
import re
import asyncio
import threading
from bot import talk, escuchar, run_selina



# Variables globales para la ventana de respuesta
response_window = None
response_text_widget = None


def escuchar_en_hilo():

    threading.Thread(target=escuchar, daemon=True).start()

# Iniciar el asistente en un hilo separado
def iniciar_asistente():
    """Función que inicia la escucha y el asistente en paralelo"""
    escuchar_en_hilo()  # Iniciar escucha en un hilo separado
    threading.Thread(target=run_selina, daemon=True).start()  # Ejecutar comandos en otro hilo

# Llamar a la función para iniciar el asistente en paralelo
iniciar_asistente()

# Agregar hablar en un hilo separado para evitar bloqueo
def hablar_respuesta(text):
    threading.Thread(target=talk, args=(text,), daemon=True).start()




# Función para manejar el doble clic en el muñeco
def show_combined_window(root):
    class CombinedWindow:
        def __init__(self, parent):
            self.complete_text = ""
            self.window = tk.Toplevel(parent)
            self.window.title("NoBt GPT \U0001F4BB")

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            window_width, window_height = 850, 750
            position_x = (screen_width // 2) - (window_width // 2)
            position_y = (screen_height // 2) - (window_height // 2)
            self.window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

            self.window.configure(bg='white')
            

            frame = tk.Frame(self.window, bg='white')
            frame.pack(expand=True, fill='both')

            # Área de respuesta
            self.response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
            self.response_frame.pack(expand=True, fill='both', padx=20, pady=20)

            self.response_frame.grid_rowconfigure(0, weight=1)
            self.response_frame.grid_columnconfigure(0, weight=1)

            scrollbar = tk.Scrollbar(self.response_frame, orient="vertical")
            scrollbar.grid(row=0, column=1, sticky='ns')

            self.response_text_widget = tk.Text(
                self.response_frame, 
                bg='#ebe8e8', 
                wrap='word',
                font=("Inter", 14), 
                padx=20, 
                pady=20, 
                bd=0, 
                state="disabled",
                yscrollcommand=scrollbar.set
            )
            self.response_text_widget.grid(row=0, column=0, sticky='nsew')

            scrollbar.config(command=self.response_text_widget.yview)

            self.setup_text_styles()

            # Área de entrada
            self.input_frame = tk.Frame(self.window, bg='white')
            self.input_frame.pack(fill='x', padx=20, pady=10)

            button_container = tk.Frame(self.input_frame, bg='white')
            button_container.pack(side='right', fill='y')

            send_button = tk.Button(button_container, text="Enviar", command=self.send_message,
                                    bg='#0A66C2', fg='white', font=("Comic Sans MS", 12))
            send_button.pack(side='left', padx=5)

            mic_button = tk.Button(button_container, text="🎤", command=iniciar_asistente,
                                   bg='#0A66C2', fg='white', font=("Comic Sans MS", 12))
            mic_button.pack(side='left', padx=5)

            self.text_widget = tk.Text(self.input_frame, font=("Comic Sans MS", 13), wrap='word', height=1,
                                       spacing1=5, spacing3=5, padx=10, highlightthickness=0, bd=1, relief='solid')
            self.text_widget.pack(side='left', fill='x', expand=True)
            self.text_widget.bind("<Return>", lambda event: self.send_message())

            self.window.after(100, lambda: self.text_widget.focus_set())

        def setup_text_styles(self):
            self.response_text_widget.tag_configure("code", font=("Courier", 12, "bold"), background="#f4f4f4")
            self.response_text_widget.tag_configure("h1md", font=("Segoe UI", 24, "bold"))
            self.response_text_widget.tag_configure("h2md", font=("Helvetica", 20, "bold"))
            self.response_text_widget.tag_configure("h3md", font=("Times New Roman", 20, "bold"))
            self.response_text_widget.tag_configure("italic", font=("Segoe UI", 12, "italic"), foreground="grey")
            self.response_text_widget.tag_configure("negrita", font=("Times New Roman", 16, "bold"))
            self.response_text_widget.tag_configure("comillas_simples", font=("Courier", 15, "bold"), foreground="grey")
            self.response_text_widget.tag_configure("code", 
                font=("Courier", 12, "bold"), 
                background="#f4f4f4",
                lmargin1=30,
                lmargin2=10,
                rmargin=30
            )

        def update_response(self, new_text):
            self.response_text_widget.config(state="normal")
            
            if "Consultando..." in self.complete_text:
                self.complete_text = self.complete_text.replace("Consultando...", "")
            self.complete_text += new_text
            
            self.response_text_widget.delete("1.0", tk.END)
            self.insert_formatted_text(self.complete_text)
            
            self.response_text_widget.yview(tk.END)
            self.response_text_widget.see("1.0")
            self.response_text_widget.config(state="disabled")

        def insert_formatted_text(self, text):
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
                    parts = re.split(r'(`[^`]+`|\*\*.*?\*\*|\*.*?\*)', line)

                    formatos = {
                        "# ": ("h1md", 1),
                        "## ": ("h2md", 2),
                        "### ": ("h3md", 3)
                    }

                    for part in parts:
                        if isinstance(part, str) and part:
                            if part.startswith("`") and part.endswith("`") and len(part) > 2:
                                self.response_text_widget.insert(tk.END, part[1:-1], "comillas_simples")
                            else:
                                header_processed = False
                                for prefijo, (tag, longitud) in formatos.items():
                                    if part.startswith(prefijo):
                                        self.response_text_widget.insert(tk.END, part[longitud:].strip(), tag)
                                        header_processed = True
                                        break
                                if not header_processed:
                                    if part.startswith("*") and part.endswith("*") and len(part) > 2 and part.count("*") == 2:
                                        self.response_text_widget.insert(tk.END, part[1:-1].strip(), "italic")
                                    elif part.startswith("**") and part.endswith("**") and len(part) > 4 and part.count("*") == 4:
                                        self.response_text_widget.insert(tk.END, part[2:-2], "negrita")
                                    else:
                                        self.response_text_widget.insert(tk.END, part)
                    self.response_text_widget.insert(tk.END, "\n\n")

        def insert_code_block(self, text):
            self.response_text_widget.insert(tk.END, "\n\n", "code")
            self.response_text_widget.insert(tk.END, text, "code")
            self.response_text_widget.insert(tk.END, "\n\n", "code")
            self.response_text_widget.insert(tk.END, "\n\n")

        def send_message(self):
            user_input = self.text_widget.get("1.0", tk.END).strip()
            if user_input:
                self.text_widget.delete("1.0", tk.END)
                self.complete_text = "" 
                self.response_text_widget.config(state="normal")
                self.response_text_widget.delete("1.0", tk.END)
                self.response_text_widget.config(state="disabled")
                self.update_response("Consultando...")
                self.window.after(100, lambda: fetch_response(user_input, self))

        def start_listening(user_input, self):
            self.window.after(100, lambda: fetch_response(user_input, self))

    return CombinedWindow(root)



def fetch_response(user_input, response_window_instance):
    def run_agent():
        response = asyncio.run(agent(user_input))  # Obtener respuesta del asistente
        response_window_instance.update_response(response)
        hablar_respuesta(response)  # Hablar la respuesta usando el bot de voz

    threading.Thread(target=run_agent, daemon=True).start()  # Ejecutar en segundo plano

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

    Frame(animation_menu, bg='#0A66C2').pack(expand=True, fill='both')

    button_config = {
        "bg": "white",
        "fg": "black",
        "font": ("Microsoft Sans Serif", 12),
        "width": 25  # Ancho fijo para todos los botones (ajusta según necesidad)
    }

    # Creación de botones con configuración uniforme
    Button(animation_menu, text="Gravedad", command=lambda: select_animation("Gravedad"), **button_config).pack(pady=10, padx=20)
    Button(animation_menu, text="izquierda", command=lambda: select_animation("Mover a la izquierda"), **button_config).pack(pady=10, padx=20)
    Button(animation_menu, text="derecha", command=lambda: select_animation("Mover a la derecha"), **button_config).pack(pady=10, padx=20)
    Button(animation_menu, text="Escalar", command=lambda: select_animation("Escalar"), **button_config).pack(pady=10, padx=20)
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
    muneco_label.bind("<Double-1>", lambda event: show_combined_window(root))
    muneco_label.bind("<ButtonRelease-3>", lambda event: show_animation_menu(event, root, muneco_label, fall_images, walk_images, climb_images, fly_image, muneco_photo))
    
    # Bind Ctrl+Q to close the application
    root.bind("<Control-q>", lambda event: [print("Bye Bye Camarada"), root.destroy()])
    

    return muneco_label, images

if __name__ == "__main__":
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()