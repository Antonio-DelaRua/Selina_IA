import tkinter as tk
from PIL import Image, ImageTk
import platform
import ctypes
import ctypes.util

# Función para configurar la transparencia según el SO

def configure_transparency(root):
    system = platform.system()
    if system == "Windows":
        root.overrideredirect(True)
        root.attributes("-transparentcolor", "white")
        root.attributes("-topmost", True)
    elif system == "Linux":
        root.overrideredirect(True)
        root.attributes("-alpha", 0.0)
        root.attributes("-topmost", True)

        # Hack para click-through en Linux (X11)
        import ctypes
        x11 = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11"))
        xfixes = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Xfixes"))

        display = x11.XOpenDisplay(None)
        window_id = root.winfo_id()

        ShapeInput = 2
        ShapeSet = 0

        xfixes.XFixesSetWindowShapeRegion(display,
                                          window_id,
                                          ShapeInput,
                                          0, 0,
                                          ctypes.c_void_p(0),
                                          ShapeSet)

# --- Setup GUI completo ---
def setup_gui(root):
    configure_transparency(root)

    images = load_images()
    muneco_photo = images["muneco"]

    # Crear Canvas transparente
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Label del muñeco
    muneco_label = tk.Label(canvas, image=muneco_photo, bg='white')
    muneco_label_window = canvas.create_window(100, 100, window=muneco_label)

    # Eventos
    muneco_label.bind("<Button-1>", start_move)
    muneco_label.bind("<B1-Motion>", lambda e: do_move(e, muneco_label, root))
    muneco_label.bind("<Double-Button-1>", lambda e: on_muneco_double_click(e, root))

    return muneco_label, images


def load_images():
    images = {
        "muneco": ImageTk.PhotoImage(Image.open("img/muneco.png").resize((200, 200), Image.LANCZOS)),
        "fall": [ImageTk.PhotoImage(Image.open(f"img/fall_{i}.png").resize((200, 200), Image.LANCZOS)) for i in range(1,4)],
        # Añadir aquí otras imágenes si las tienes
    }
    return images

# Para mover el muñeco
startX, startY = 0, 0

def start_move(event):
    global startX, startY
    startX, startY = event.x, event.y

def do_move(event, muneco_label, root):
    x = event.x_root - startX
    y = event.y_root - startY
    muneco_label.place(x=x, y=y)

# Para manejar doble clic (mostrar input)
def on_muneco_double_click(event, root):
    input_window = tk.Toplevel(root)
    input_window.geometry("400x100")

    entry = tk.Entry(input_window, font=("Arial", 14))
    entry.pack(fill="both", expand=True, padx=20, pady=20)

    send_button = tk.Button(input_window, text="Enviar", command=lambda: print("Enviar mensaje"))
    send_button.pack()
