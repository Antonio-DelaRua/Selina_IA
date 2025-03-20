import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame
from PIL import Image, ImageTk
import threading
from agent import agent
from movimientos import apply_gravity, move_to_edge, climb_animation
import re

# Variables globales para la ventana de respuesta y el widget de texto
response_window = None
response_text_widget = None

def on_muneco_double_click(event, root):

    # Crea una nueva ventana de entrada cuando se hace doble clic en el muñeco
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

    # Configurar la geometría y el color de fondo de la ventana de entrada
    input_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    input_window.configure(bg='white')

    # Crear un marco dentro de la ventana de entrada
    frame = tk.Frame(input_window, bg='white')
    frame.pack(pady=10, padx=10, expand=True, fill='both')

    # Botón de enviar para enviar el mensaje
    send_button = tk.Button(frame, text="Enviar", command=lambda: send_message(input_window, root, text_widget), bg='orange', fg='white', font=("Comic Sans MS", 12))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    # Área de texto para que el usuario ingrese su mensaje
    text_widget = tk.Text(frame, font=("Comic Sans MS", 13), wrap='word', height=1, spacing1=5, spacing3=5, padx=10, highlightthickness=0, bd=1, relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)

    # Detectar cambios en el texto para ajustar dinámicamente
    text_widget.bind("<KeyRelease>", lambda event: on_text_change(event, text_widget))

    # Enviar el mensaje al presionar Enter
    text_widget.bind("<Return>", lambda event: send_message(input_window, root, text_widget))

    # Permitir saltos de línea con Shift + Enter
    text_widget.bind("<Shift-Return>", lambda event: None)

    # Establecer el foco en el área de texto automáticamente
    text_widget.focus_set()

def send_message(input_window, root, text_widget):
    # Obtener el texto ingresado por el usuario
    user_text = text_widget.get("1.0", tk.END).strip()
    if user_text:
        # Mostrar la ventana de respuesta si no está abierta
        response_window_instance = show_response(root)

        # Mostrar el mensaje de "Consultando..." mientras se procesa la respuesta
        response_window_instance.update_response("Consultando...")  # Mostrar mensaje de espera

        # Usar el agente para obtener una respuesta en un hilo separado
        threading.Thread(target=fetch_response, args=(user_text, response_window_instance)).start()

     # Cerrar la ventana de entrada después de enviar el mensaje   
    input_window.destroy()

def fetch_response(user_text, response_window_instance):
     # Obtener la respuesta del "agente" (lógica que procesa el mensaje)
    response = agent(user_text)

    # Si no hay respuesta, mostrar un mensaje predeterminado
    if response is None:
        response = "Lo siento, no pude obtener una respuesta en este momento."

    # Actualizar la ventana de respuesta con el resultado
    response_window_instance.update_response(response)

def on_text_change(event, text_widget):
    content = text_widget.get("1.0", tk.END)
    lines = content.count('\n') + 1
    new_height = min(10, lines)  # Limitar a un máximo de 10 líneas visibles
    text_widget.config(height=new_height)


def show_response(root):
    # Declaramos las variables globales para acceder a la ventana de respuesta y al widget de texto
    global response_window, response_text_widget

    # Función para copiar texto al portapapeles
    def copy_to_clipboard(text):
        root.clipboard_clear()  # Limpia el contenido actual del portapapeles
        root.clipboard_append(text)  # Agrega el texto al portapapeles
        root.update()  # Actualiza la ventana principal para aplicar los cambios

    # Clase que maneja la ventana de respuesta
    class ResponseWindow:
        def __init__(self, text_widget):
            self.text_widget = text_widget  # Widget de texto donde se mostrará la respuesta
            self.complete_text = ""  # Almacena todo el texto de la respuesta

        # Método para actualizar el contenido de la respuesta
        def update_response(self, new_text):
            # Elimina el mensaje "Consultando..." si está presente
            if "Consultando..." in self.complete_text:
                self.complete_text = self.complete_text.replace("Consultando...", "")

            self.complete_text += new_text  # Añade el nuevo texto a la respuesta completa

            # Borra el contenido anterior del widget de texto
            self.text_widget.delete("1.0", tk.END)

            # Inserta el texto formateado actualizado
            self.insert_formatted_text(self.complete_text)

            # Desplaza la vista del widget al final para mostrar el nuevo contenido
            self.text_widget.yview(tk.END)

            # Fuerza la actualización visual del widget
            self.text_widget.update_idletasks()

            # Asegura que el texto visible comience desde el inicio
            self.text_widget.see("1.0")

        # Método para insertar texto formateado en el widget de texto
        def insert_formatted_text(self, text):
            # Borra el contenido previo del widget
            self.text_widget.delete("1.0", tk.END)

            # Divide el texto en líneas
            lines = text.split('\n')

            # Variables para detectar bloques de código
            in_code_block = False
            code_block_text = ""

            # Recorre cada línea de texto
            for line in lines:
                # Detecta el inicio o fin de un bloque de código (```)
                if line.startswith("```"):
                    if in_code_block:  # Si ya estamos en un bloque de código, lo cerramos
                        self.insert_code_block(code_block_text)  # Insertamos el bloque de código
                        in_code_block = False
                        code_block_text = ""  # Reseteamos el texto del bloque de código
                    else:
                        in_code_block = True  # Indicamos que estamos dentro de un bloque de código

                elif in_code_block:
                    code_block_text += line + "\n"  # Acumulamos las líneas dentro del bloque de código

                else:
                    # Diccionario con formatos para encabezados (Markdown)
                    formatos = {
                        "# ": ("h1md", 1),
                        "## ": ("h2md", 2),
                        "### ": ("h3md", 3)
                    }

                    # Dividimos el texto por negrita (**) o cursiva (*) usando una expresión regular
                    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line)

                    for part in parts:
                        if isinstance(part, str) and part:  # Si es un fragmento de texto no vacío
                            header_processed = False

                            # Procesamos los encabezados (h1, h2, h3)
                            for prefijo, (tag, longitud) in formatos.items():
                                if part.startswith(prefijo):
                                    # Inserta el texto del encabezado con el formato correspondiente
                                    self.text_widget.insert(tk.END, part[longitud:].strip(), tag)
                                    header_processed = True
                                    break

                            # Si no es un encabezado, verificamos si es negrita o cursiva
                            if not header_processed:
                                if part.startswith("*") and part.endswith("*") and len(part) > 2 and part.count("*") == 2:
                                    self.text_widget.insert(tk.END, part[1:-1].strip(), "italic")
                                elif part.startswith("**") and part.endswith("**") and len(part) > 4 and part.count("*") == 4:
                                    self.text_widget.insert(tk.END, part[2:-2], "negrita")
                                else:
                                    # Inserta el texto normal
                                    self.text_widget.insert(tk.END, part)

                    # Agrega un salto de línea después de cada línea procesada
                    self.text_widget.insert(tk.END, "\n")

        # Método para insertar un bloque de código formateado
        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n\n", "code")  # Línea en blanco antes del bloque
            self.text_widget.insert(tk.END, text, "code")  # Inserta el bloque de código
            self.text_widget.insert(tk.END, "\n\n", "code")  # Línea en blanco después del bloque

    # Verifica si la ventana de respuesta ya existe
    if response_window is None or not response_window.winfo_exists():
        # Crea una nueva ventana secundaria (Toplevel) para mostrar la respuesta
        response_window = tk.Toplevel(root)
        response_window.title("NoBt GPT  \U0001F4BB")  # Título con un emoji

        # Centra la ventana en la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Configura el fondo de la ventana como blanco
        response_window.configure(bg='white')

        # Mantiene la ventana de respuesta siempre encima de la principal
        response_window.attributes("-topmost", True)

        # Crea un marco principal dentro de la ventana de respuesta
        frame = tk.Frame(response_window, bg='white')
        frame.pack(expand=True, fill='both')

        # Crea un marco para contener el widget de texto con borde
        response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
        response_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Crea el widget de texto donde se mostrará el contenido
        response_text_widget = tk.Text(response_frame, bg='#ebe8e8', wrap='word', font=("Inter", 14), padx=20, pady=20, 
                                      spacing1=10, spacing2=12, spacing3=15, bd=0)

        # Método para insertar un bloque de código formateado
        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n\n", "code")
            self.text_widget.insert(tk.END, text, "code")
            self.text_widget.insert(tk.END, "\n\n", "code")

    # Verifica si la ventana de respuesta ya existe
    if response_window is None or not response_window.winfo_exists():
        # Crea una nueva ventana secundaria (Toplevel) para mostrar la respuesta
        response_window = tk.Toplevel(root)
        response_window.title("NoBt GPT  \U0001F4BB")   # Título con un emoji

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

         # Configura el fondo de la ventana como blanco
        response_window.configure(bg='white')

        # Mantiene la ventana de respuesta siempre encima de la principal
        response_window.attributes("-topmost", True)

        # Crea un marco principal dentro de la ventana de respuesta
        frame = tk.Frame(response_window, bg='white')
        frame.pack(expand=True, fill='both')

        # Crea un marco para contener el widget de texto con borde
        response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
        response_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Crea el widget de texto donde se mostrará el contenido
        response_text_widget = tk.Text(response_frame, bg='#ebe8e8', wrap='word', font=("Inter", 14), padx=20, pady=20, 
                                      spacing1=10, spacing2=12, spacing3=15, bd=0)
        
        
        # Configure tags on the actual Text widget

        # Estilo formateado del codigo (``` ```)
        response_text_widget.tag_configure("code", 
                font=("Courier", 12), 
                background="#f4f4f4",
                lmargin1=30,   # 30 píxeles de margen izquierdo
                lmargin2=10,   # 30 píxeles para líneas que se parten
                rmargin=30     # 30 píxeles de margen derecho
            )
            
        # Estilo para encabezado 1 (#)
        response_text_widget.tag_configure("h1md",
            font=("Segoe UI", 30, "bold"),           # Fuente grande y en negrita
            foreground="#1a1a1a",                    # Color oscuro para el texto
            spacing1=0,                              ## Espacio superior
            spacing3=0,                              # Espacio inferior
            lmargin1=0,                              # Sin margen izquierdo
            lmargin2=0,                              # Sin margen izquierdo para líneas adicionales
            
        )

        # Estilo para encabezado 2 (##)
        response_text_widget.tag_configure("h2md",
            font=("Helvetica", 24, "bold"),          # Fuente mediana y en negrita
            foreground="#3a3a3a",                    # Color gris oscuro
            spacing1=20,                             # Espacio superior
            spacing3=12,                             # Espacio inferior
            underline=True,                          # Subrayado
            justify="left"                           # Alineación a la izquierda
        )

        # Estilo para encabezado 3 (###)
        response_text_widget.tag_configure("h3md",
            font=("Segoe UI", 18, "bold"),           # Fuente más pequeña y en negrita
            foreground="#3a3a3a",                    # Color gris oscuro

        )

        # Estilo para cursiva (*texto*)
        response_text_widget.tag_configure("italic",
            font=("Segoe UI", 12, "italic"),          # Fuente en cursiva
            foreground="#444444"                      # Color gris medio
        )

        # Estilo para negrita (**texto**)
        response_text_widget.tag_configure("negrita",
            font=("Times New Roman", 16, "bold")      # Fuente más grande y en negrita
        )

        # Empaquetar el widget de texto para expandirse y llenar el espacio disponible
        response_text_widget.pack(expand=True, fill='both')

        # Asignar un atajo de teclado (Ctrl+Espacio) para copiar el contenido al portapapeles
        response_window.bind("<Control-space>", lambda event: copy_to_clipboard(response_text_widget.get("1.0", tk.END)))

    return ResponseWindow(response_text_widget)


# Función para registrar la posición inicial del movimiento
def start_move(event):
    global startX, startY
    startX = event.x
    startY = event.y


# Función para mover un widget dentro de los límites de la pantalla
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


# Función para mostrar  menú de selección de animación
def show_animation_menu(event, root, muneco_label, fall_images, walk_images, climb_images, fly_image, muneco_photo):
    def select_animation(animation):
        if animation == "Gravedad":
            apply_gravity(muneco_label, root, fall_images, muneco_photo)
        elif animation == "Mover a la izquierda":
            move_to_edge("left", muneco_label, root, walk_images, muneco_photo)
        elif animation == "Mover a la derecha":
            move_to_edge("right", muneco_label, root, walk_images, muneco_photo)
        elif animation == "Escalar":
            climb_animation(muneco_label, root, climb_images, fly_image, muneco_photo)
        animation_menu.destroy()

    # Crear una ventana emergente para el menú de animación
    animation_menu = Toplevel(root)
    animation_menu.title("Seleccionar Animación")

    # Determinar la posición del menú basado en la posición del muñeco
    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()
    menu_width = 200
    menu_height = 240
    position_x = x + muneco_label.winfo_width()
    position_y = y

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Ajustar la posición horizontal del menú si está cerca del borde derecho de la pantalla
    if position_x + menu_width > screen_width:
        position_x = x - menu_width

    # Ajustar la posición horizontal del menú si está cerca del borde izquierdo de la pantalla
    if position_x < 0:
        position_x = x + muneco_label.winfo_width()

    # Ajustar la posición vertical del menú si está cerca del borde inferior de la pantalla
    if position_y + menu_height > screen_height:
        position_y = screen_height - menu_height - 10

    # Establecer la geometría y el color de fondo del menú
    animation_menu.geometry(f"{menu_width}x{menu_height}+{position_x}+{position_y}")
    animation_menu.configure(bg='white')

     # Agregar opciones al menú de animación
    Frame(animation_menu, bg='white').pack(expand=True, fill='both')

    Button(animation_menu, text="Gravedad", command=lambda: select_animation("Gravedad"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la izquierda", command=lambda: select_animation("Mover a la izquierda"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Mover a la derecha", command=lambda: select_animation("Mover a la derecha"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    Button(animation_menu, text="Escalar", command=lambda: select_animation("Escalar"), bg='orange', fg='white', font=("Microsoft Sans Serif", 12)).pack(pady=10)
    
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
    root.bind("<Control-q>", lambda event: root.quit())
    

    return muneco_label, images

if __name__ == "__main__":
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()