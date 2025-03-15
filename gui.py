import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QPushButton,
                             QDialog, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from chatbot import chat_with_bot

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
def animate_move(window, target_x, timer):
    step = 10 if window.x() < target_x else -10

    def move_step():
        current_x = window.x()
        if (step > 0 and current_x < target_x) or (step < 0 and current_x > target_x):
            window.move(current_x + step, window.y())
        else:
            timer.stop()

    timer.timeout.connect(move_step)
    timer.start(30)
# Mantener referencias globales
open_windows = []

# Ventana de chat
def open_chat_window():
    input_dialog = QDialog()
    input_dialog.setWindowTitle("Chat")
    input_dialog.setGeometry(100, 100, 400, 300)

    layout = QVBoxLayout()

    entry = QLineEdit()
    response_display = QTextEdit()
    response_display.setReadOnly(True)

    def update_callback(new_text):
        response_display.insertPlainText(new_text)

    def finish_callback():
        response_display.append("\n-----------------------")

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

    # Guardar referencia para evitar cierre inesperado
    open_windows.append(input_dialog)
# Ventana de controles
def open_control_window(window, screen_geometry):
    menu = QDialog()
    menu.setWindowTitle("Seleccionar Animación")

    # Calcular posición de la ventana al lado del muñeco
    x = window.x() + window.width()
    y = window.y()

    menu_width, menu_height = 200, 250
    if y + menu.height() > screen_geometry.height():
        y = screen_geometry.height() - menu.height() - 10

    menu.setGeometry(x, y, menu_width, menu_height)

    layout = QVBoxLayout()

    btn_gravity = QPushButton("Gravedad")
    btn_left = QPushButton("Mover a la izquierda")
    btn_right = QPushButton("Mover a la derecha")
    btn_climb = QPushButton("Escalar")

    gravity_timer = QTimer()
    gravity_timer.timeout.connect(lambda: apply_gravity(window, screen_geometry, gravity_timer))
    btn_gravity.clicked.connect(lambda: gravity_timer.start(30))

    move_timer = QTimer()
    btn_left.clicked.connect(lambda: animate_move(window, 0, move_timer))
    btn_right.clicked.connect(lambda: animate_move(window, screen_geometry.width() - window.width(), move_timer))
    # Puedes implementar la animación escalar aquí
    btn_climb.clicked.connect(lambda: print("Animación escalar no implementada aún."))

    for btn in [btn_gravity, btn_left, btn_right, btn_climb]:
        menu.layout().addWidget(btn) if menu.layout() else menu.setLayout(QVBoxLayout())
        menu.layout().addWidget(btn)

    menu.setGeometry(x, y, menu.sizeHint().width(), menu.sizeHint().height())
    menu.exec_()


# Setup GUI
def setup_gui():
    app = QApplication(sys.argv)

    images = load_images()
    muneco_photo = images["muneco"]

    window = QLabel()
    window.setPixmap(muneco_photo)
    window.resize(muneco_photo.size())

    configure_transparency(window)

    screen_geometry = QApplication.primaryScreen().geometry()
    initial_x = (screen_geometry.width() - muneco_photo.width()) // 2
    window.move(initial_x, 0)

    start_pos = None

    def mousePressEvent(event): # Abrir ventana de controles al hacer clic derecho
        global start_pos
        if event.button() == Qt.RightButton:
            print("Abrir ventana de controles")
            open_control_window(window, screen_geometry)
        elif event.button() == Qt.LeftButton:
            print("Iniciar movimiento")
            start_pos = event.globalPos()

    def mouseMoveEvent(event): # Mover la ventana al arrastrar
        global start_pos
        if start_pos:
            print("Mover ventana")
            delta = event.globalPos() - start_pos
            window.move(window.pos() + delta)
            start_pos = event.globalPos()

    def mouseDoubleClickEvent(event): # Abrir ventana de chat al hacer doble clic
        if event.button() == Qt.LeftButton:
           print("Abrir ventana de chat")
           open_chat_window()

    window.mouseDoubleClickEvent = mouseDoubleClickEvent
    window.mousePressEvent = mousePressEvent
    window.mouseMoveEvent = mouseMoveEvent

    gravity_timer = QTimer()
    gravity_timer.timeout.connect(lambda: apply_gravity(window, screen_geometry, gravity_timer))
    gravity_timer.start(30)

    window.show()
    sys.exit(app.exec_())
