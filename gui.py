import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QPushButton,
                             QDialog, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from chatbot import chat_with_bot


from tkintermd.frame import TkintermdFrame
from tkinterweb import HtmlFrame
import markdown
import tempfile

import tkinter as tk
from tkinter.constants import *



open_windows = []
# Configurar transparencia (sin click-through para permitir interacción)
def configure_transparency(window):
    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    window.setAttribute(Qt.WA_TranslucentBackground, True)

# Método original adaptado correctamente a PyQt5
def load_images():
    image_paths = {
        "muneco": "img/muneco.png",
        "fall": [f"img/fall_{i}.png" for i in range(1, 4)],
        "walk_left": [f"img/walk_left_{i}.png" for i in range(1, 4)],
        "climb": [f"img/climb_{i}.png" for i in range(1, 4)],
        "fly": "img/volar.png"
    }

    images = {}

    for key, paths in image_paths.items():
        if isinstance(paths, list):
            images[key] = [QPixmap(path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation) for path in paths]
        else:
            images[key] = QPixmap(paths).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return images

# Aplicar gravedad al muñeco hasta llegar al borde inferior
def apply_gravity(window, screen_geometry, timer):
    y = window.y()
    if y < screen_geometry.height() - window.height():
        window.move(window.x(), y + 5)
    else:
        timer.stop()

# Animaciones de movimiento lateral
def animate_move(window, target_x):
    move_timer = QTimer()
    step = 10 if target_x > window.x() else -10  # corregido aquí

    def move_step():
        current_x = window.x()
        if (step > 0 and current_x < target_x) or (step < 0 and current_x > target_x):
            window.move(current_x + step, window.y())
        else:
            move_timer.stop()

    move_timer.timeout.connect(move_step)
    move_timer.start(30)


# Ventana de chat
def open_chat_window():
    input_dialog = QDialog()
    input_dialog.setWindowTitle("Chat")
    input_dialog.setGeometry(100, 100, 400, 300)
    input_dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint  | Qt.Tool)

    layout = QVBoxLayout()

    entry = QLineEdit()
    response_display = QTextEdit()
    response_display.setReadOnly(True)

    def update_callback(new_text):
        # Create a new Tkinter window for the response
        root = tk.Tk()
        frame = HtmlFrame(root, messages_enabled=False)

        # Load the HTML template with CSS styles
        style = open("template.html").read()

        # Create HTML content
        body_start = '<body>'
        body_end = '</body>'

        # Write the HTML content combining style and markdown-converted text
        # Remove code blocks markers if present
        f = tempfile.NamedTemporaryFile(mode='w')
        f.write(style + body_start + new_text.replace("```", "") + body_end)
        f.flush()

        # Load the HTML file into the frame
        frame.load_file(f.name)
        frame.pack(fill="both", expand=True)
        root.mainloop()

    def finish_callback():
        response_display.append("\n--- Fin del mensaje ---")

    def send_message():
        user_message = entry.text()
        response_display.append(f"Tú: {user_message}")
        chat_with_bot(user_message, update_callback, finish_callback)
        entry.clear()

    send_button = QPushButton("Enviar")
    send_button.clicked.connect(send_message)

    layout.addWidget(entry)
    layout.addWidget(send_button)
    layout.addWidget(response_display)

    input_dialog.setLayout(layout)
    input_dialog.show()
    # Save global reference
    open_windows.append(input_dialog)



# Animación para escalar
def climb_animation(window, screen_geometry, climb_images, fly_image):
    climb_timer = QTimer()
    current_frame = [0]  # Para mantener la referencia del frame actual
    climb_step = 8  # Velocidad vertical de la escalada
    frame_count = 2

    def climbing_step():
        if window.y() > 0:
            window.setPixmap(climb_images[current_frame[0] % frame_count])
            window.move(window.x(), window.y() - climb_step)
            current_frame[0] += 1
        else:
            window.setPixmap(fly_image)
            climb_timer.stop()

    climb_timer.timeout.connect(climbing_step)
    climb_timer.start(100)  # intervalo en milisegundos entre frames


# Ventana de controles
def show_animation_menu(window, screen_geometry, images):
    animation_menu = QDialog()
    animation_menu_width, animation_menu_height = 200, 250
    x = window.x() + window.width()
    y = window.y()
    if y + animation_menu_height > screen_geometry.height():
        y = screen_geometry.height() - animation_menu_height - 10
    animation_menu_position = f"{animation_menu_width}x{animation_menu_height}+{x}+{y}"

    animation_menu = QDialog()
    animation_menu.setWindowTitle("Seleccionar Animación")
    animation_menu.setGeometry(x, y, animation_menu_width, animation_menu_height)
    animation_menu.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.Tool)

    layout = QVBoxLayout()

    def select_animation(animation):
        if animation == "Gravedad":
            gravity_timer = QTimer()
            gravity_timer.timeout.connect(lambda: apply_gravity(window, screen_geometry, gravity_timer))
            gravity_timer.start(30)
        elif animation == "Mover a la izquierda":

            animate_move(window, 0)
        elif animation == "Mover a la derecha":

            animate_move(window, screen_geometry.width() - window.width())
        elif animation == "Escalar":
             climb_animation(window, screen_geometry, images["climb"], images["muneco"])




    btn_gravity = QPushButton("Gravedad")
    btn_gravity.clicked.connect(lambda: select_animation("Gravedad"))

    btn_left = QPushButton("Mover a la izquierda")
    btn_left.clicked.connect(lambda: select_animation("Mover a la izquierda"))

    btn_right = QPushButton("Mover a la derecha")
    btn_right.clicked.connect(lambda: select_animation("Mover a la derecha"))

    btn_climb = QPushButton("Escalar")
    btn_climb.clicked.connect(lambda: select_animation("Escalar"))

    layout.addWidget(btn_gravity)
    layout.addWidget(btn_left)
    layout.addWidget(btn_right)
    layout.addWidget(btn_climb)

    animation_menu.setLayout(layout)
    animation_menu.exec_()
    # Guardar referencia global
    open_windows.append(animation_menu)

# Setup GUI

app = QApplication(sys.argv)
window = QLabel()

def setup_gui():
    images = load_images() # Cargar imágenes
    muneco_photo = images["muneco"]
    window.setPixmap(muneco_photo) # Establecer imagen de muñeco
    window.resize(muneco_photo.size()) # Establecer tamaño de la ventana

    configure_transparency(window)

    screen_geometry = app.primaryScreen().geometry()
    initial_x = (screen_geometry.width() - muneco_photo.width()) // 2
    window.move(initial_x, 0)

    gravity_timer = QTimer()
    gravity_timer.timeout.connect(lambda: apply_gravity(window, screen_geometry, gravity_timer))
    gravity_timer.start(30)

    # Variables para mover muñeco arrastrando
    start_pos = None

    def mousePressEvent(event):
        nonlocal start_pos
        if event.button() == Qt.RightButton:
            show_animation_menu(window, screen_geometry, images)
        elif event.button() == Qt.LeftButton:
            start_pos = event.globalPos()

    def mouseMoveEvent(event):
        nonlocal start_pos
        if start_pos:
            delta = event.globalPos() - start_pos
            window.move(window.pos() + delta)
            start_pos = event.globalPos()

    def mouseDoubleClickEvent(event):
        if event.button() == Qt.LeftButton:
            open_chat_window()

    window.mousePressEvent = mousePressEvent
    window.mouseDoubleClickEvent = mouseDoubleClickEvent
    window.mouseMoveEvent = mouseMoveEvent

    # Gravedad automática al iniciar
    gravity_timer = QTimer()
    gravity_timer.timeout.connect(lambda: apply_gravity(window, screen_geometry, gravity_timer))
    gravity_timer.start(30)

    window.show()
    sys.exit(app.exec_())