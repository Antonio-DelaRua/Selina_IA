import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame
from PIL import Image, ImageTk
import threading
from agent import agent
from movimientos import apply_gravity, move_to_edge, climb_animation

response_window = None
response_text_widget = None

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

    send_button = tk.Button(frame, text="Enviar", command=lambda: send_message(input_window, root, text_widget), bg='orange', fg='white', font=("Comic Sans MS", 12))
    send_button.pack(side='left', padx=10, pady=10, fill='y')

    text_widget = tk.Text(frame, font=("Comic Sans MS", 13), wrap='word', height=1, spacing1=5, spacing3=5, padx=10, highlightthickness=0, bd=1, relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)
    text_widget.bind("<KeyRelease>", lambda event: on_text_change(event, text_widget))
    text_widget.bind("<Return>", lambda event: send_message(input_window, root, text_widget))
    text_widget.bind("<Shift-Return>", lambda event: None)

    text_widget.focus_set()

def send_message(input_window, root, text_widget):
    user_text = text_widget.get("1.0", tk.END).strip()
    if user_text:
        response_window_instance = show_response(root)
        response_window_instance.update_response("Consultando...")  # Mostrar mensaje de espera

        # Usar el agente para obtener una respuesta en un hilo separado
        threading.Thread(target=fetch_response, args=(user_text, response_window_instance)).start()
    input_window.destroy()

def fetch_response(user_text, response_window_instance):
    response = agent(user_text)
    if response is None:
        response = "Lo siento, no pude obtener una respuesta en este momento."
    response_window_instance.update_response(response)

def on_text_change(event, text_widget):
    content = text_widget.get("1.0", tk.END)
    lines = content.count('\n') + 1
    new_height = min(10, lines)  # Limitar a un máximo de 10 líneas visibles
    text_widget.config(height=new_height)

def show_response(root):
    global response_window, response_text_widget

    def copy_to_clipboard(text):
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()  # Actualizar el portapapeles

    class ResponseWindow:
        def __init__(self, text_widget):
            self.text_widget = text_widget
            self.complete_text = ""

        def update_response(self, new_text):
            if "Consultando..." in self.complete_text:
                self.complete_text = self.complete_text.replace("Consultando...", "")
            self.complete_text += new_text
            self.text_widget.delete("1.0", tk.END)  # Eliminar el texto existente
            self.insert_formatted_text(self.complete_text)
            self.text_widget.yview(tk.END)  # Desplazar la vista hacia el final del texto
            self.text_widget.update_idletasks()
            self.text_widget.see("1.0")  # Asegurar que el texto comience desde el principio

        def insert_formatted_text(self, text):
            self.text_widget.delete("1.0", tk.END)  # Eliminar el texto existente
            lines = text.split('\n')
            in_code_block = False
            code_block_text = ""

            for line in lines:
                if line.startswith("```"):
                    if in_code_block:
                        # End of code block
                        self.insert_code_block(code_block_text)
                        in_code_block = False
                        code_block_text = ""
                    else:
                        # Start of code block
                        in_code_block = True
                elif in_code_block:
                    code_block_text += line + "\n"
                else:
                    parts = line.split('**')
                    for i, part in enumerate(parts):
                        if i % 2 == 0:
                            # Texto normal
                            self.text_widget.insert(tk.END, part)
                        else:
                            # Texto en negrita
                            self.text_widget.insert(tk.END, part, "bold")
                    self.text_widget.insert(tk.END, "\n")

        def insert_code_block(self, text):
            self.text_widget.insert(tk.END, "\n\n", "code")
            self.text_widget.insert(tk.END, text, "code")
            self.text_widget.insert(tk.END, "\n\n", "code")
            copy_button = tk.Button(self.text_widget, text="Copiar", command=lambda: copy_to_clipboard(text), bg='grey', fg='white', font=("Comic Sans MS", 8))
            self.text_widget.window_create(tk.END, window=copy_button)
            self.text_widget.insert(tk.END, "\n\n")

    if response_window is None or not response_window.winfo_exists():
        response_window = tk.Toplevel(root)
        response_window.title("Son Goku    孫 悟空")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 800
        window_height = 600
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        response_window.configure(bg='white')
        response_window.attributes("-topmost", True)  # Asegurar que la ventana esté siempre en la parte superior

        frame = tk.Frame(response_window, bg='white')
        frame.pack(expand=True, fill='both')

        response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
        response_frame.pack(expand=True, fill='both', padx=10, pady=10)

        response_text_widget = tk.Text(response_frame, bg='#ebe8e8', wrap='word', font=("Inter", 14), padx=20, pady=20, spacing1=5, spacing3=5, bd=0)
        response_text_widget.tag_configure("code", font=("Courier", 12), background="#f4f4f4", spacing3=10, lmargin1=20, lmargin2=20)
        response_text_widget.tag_configure("bold", font=("Times New Roman", 14, "bold"))

        response_text_widget.pack(expand=True, fill='both')

        response_window.bind("<Control-space>", lambda event: copy_to_clipboard(response_text_widget.get("1.0", tk.END)))

    return ResponseWindow(response_text_widget)

def start_move(event):
    global startX, startY
    startX = event.x
    startY = event.y

def do_move(event, muneco_label, root):
    x = muneco_label.winfo_x() + event.x - startX
    y = muneco_label.winfo_y() + event.y - startY

    if x < 0:
        x = 0
    elif x > root.winfo_width() - muneco_label.winfo_width():
        x = root.winfo_width() - muneco_label.winfo_width()

    if y < 0:
        y = 0
    elif y > root.winfo_height() - muneco_label.winfo_height():
        y = root.winfo_height() - muneco_label.winfo_height()

    muneco_label.place(x=x, y=y)

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

    animation_menu = Toplevel(root)
    animation_menu.title("Seleccionar Animación")

    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()
    menu_width = 200
    menu_height = 250
    position_x = x + muneco_label.winfo_width()
    position_y = y

    screen_height = root.winfo_screenheight()
    if position_y + menu_height > screen_height:
        position_y = screen_height - menu_height - 10

    animation_menu.geometry(f"{menu_width}x{menu_height}+{position_x}+{position_y}")
    animation_menu.configure(bg='white')

    Frame(animation_menu, bg='white').pack(expand=True, fill='both')

    Button(animation_menu, text="Gravedad", command=lambda: select_animation("Gravedad"), bg='orange', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)
    Button(animation_menu, text="izquierda", command=lambda: select_animation("Mover a la izquierda"), bg='orange', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)
    Button(animation_menu, text="derecha", command=lambda: select_animation("Mover a la derecha"), bg='orange', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)
    Button(animation_menu, text="Escalar", command=lambda: select_animation("Escalar"), bg='orange', fg='white', font=("Comic Sans MS", 12)).pack(pady=10)

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
    root.title("NoBt GPT Goku")
    root.configure(bg='white')

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
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