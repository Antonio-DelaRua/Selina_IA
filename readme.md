<div id="header" align="center">

<img src="/img/muneco.png" width="300" />

<h1 align="center">👋 SeliNa Python</h1>

<h3 aling="center">Un chat gpt dentro de un avatar3d con animaciones y mucho más.</h3>
<br>

</div>

---
<div align="center">
<h3>🔨 👦 About Me :</h3>
<br>

 💻 RuXx .

</div>


<div align="center">
<h3>🔨 Languages and Tools:</h3>
<br>
<div>
<img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/Angular_full_color_logo.svg" title="Angular" alt="Angular" width="45" height="45"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-plain-wordmark.svg" title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg" title="Javascript" alt="Javascript" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sass/sass-original.svg" title="SASS" alt="Sass" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original-wordmark.svg" title="GIT" alt="Git" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="PYTHON" alt="python" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="docker" alt="docker" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/firebase/firebase-plain-wordmark.svg" title="firebase" alt="firebase" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/java/java-original-wordmark.svg" title="java" alt="java" width="40" height="40"/>&nbsp;
</div>
</div>



## CMD
ctrl + q  ------> cerrar aplicación
kiv para moviles y tablet ( tactil )

## PALABRAS CLAVE


# predefinidos alias_dic
- hola
- entorno virtual
- git 
- react
- ruxx
- angular

 # bd_python
- que es python y para que se utiliza?
- como instalar python en windows?
- fundamentos de python
- tipos de datos basicos
- enteros
- int
- float
- numeros complejos
- complex
- cadena de texto
- str
- boolean
- listas
- set
- diccionarios
- operadores aritmeticos
- operadores logicos
- operadores de comparacion
- operadores de asignacion
- estructuras de control
- condicionales
- if
- for
- while
- continue
- pass
- break
- funcion python
- palindromo
- calculadora
- manejo de excepciones
- multiples excepciones
- excepciones anidadas
- finally
- else
- POO
- herencia
- polimorfismo
- abstraccion
- django
- flask
- spring boot
- modulo
- iterador
- decoradores
- context managers
- metaclase
- GIL
- gestion de memoria
- protocolo
- pytest
- unittest
- debugging
- logging
- flake8
- black
- Mypy
- isort
- gestor de dependencias
- packaging
- documentacion
- fastAPI
- sqlalchemy
- alembic
- OAuth2
- JWT
- graphQL
- postgresql
- mysql
- mongodb
- redis
- conexiones asincronas
- asyncpg
- aiomysql
- caching
- patrones de diseño
- singleton
- factory
- Observer
- strategy
- solid
- microservicios
- ejercicio1
- ejercicio2
- ejercicio3
- ejercicio4
- ejercicio5
- ejercicio6
- ejercicio7
- ejercicio8
- ejercicio9
- ejercicio10




me queda por documentar : {

Arquitectura limpia (Clean Architecture): Separación de capas (dominio, aplicación, infraestructura).

Microservicios vs Monolito: Cuándo elegir cada uno.

Event-Driven Architecture: Uso de brokers como RabbitMQ, Kafka.

CQRS y Event Sourcing: Diseño para sistemas complejos.

7. DevOps y Deployment
Contenedores: Docker, Docker Compose.

Cloud: AWS (EC2, S3, Lambda), GCP, Azure.

CI/CD: GitHub Actions, GitLab CI, Jenkins.

Servidores web: Nginx, Gunicorn, uWSGI.

Monitorización: Prometheus, Grafana, Sentry.

Infra as Code: Terraform, CloudFormation.

8. Seguridad
OWASP Top 10: Prevención de SQLi, XSS, CSRF, etc.

Hardening: Configuración segura de servidores y aplicaciones.

Criptografía: Uso de bcrypt, cryptography.

Auditorías: Herramientas como Bandit para análisis estático.

9. Habilidades Blandas
Trabajo en equipo: Uso de metodologías ágiles (Scrum, Kanban).

Mentoría: Guiar a desarrolladores junior.

Comunicación: Explicar ideas técnicas a no técnicos.

Gestión de tiempo: Priorización de tareas complejas.

10. Extra (Dependiendo del enfoque)
Data Science: Pandas, NumPy, Matplotlib.

Machine Learning: Scikit-learn, TensorFlow, PyTorch.

Automatización: Scripts con click o argparse.

Web Scraping: BeautifulSoup, Scrapy, Selenium.


}

Si usas Python 3.10 o superior y te da error sentence-transformers, instala también:

pip install torch torchvision torchaudio

pip install --user Cython
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









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
            self.window.attributes("-topmost", True)

            frame = tk.Frame(self.window, bg='white')
            frame.pack(expand=True, fill='both')

            # Área de respuesta
            self.response_frame = tk.Frame(frame, bg='#ebe8e8', bd=0.5, relief='solid')
            self.response_frame.pack(expand=True, fill='both', padx=20, pady=20)

            self.response_text_widget = tk.Text(self.response_frame, bg='#ebe8e8', wrap='word',
                                                font=("Inter", 14), padx=20, pady=20, bd=0, state="disabled")
            self.response_text_widget.pack(expand=True, fill='both')

            # Barra de desplazamiento
            scrollbar = tk.Scrollbar(self.response_frame, orient="vertical", command=self.response_text_widget.yview)
            scrollbar.pack(side="right", fill="y")
            self.response_text_widget.config(yscrollcommand=scrollbar.set)

            # Área de entrada
            self.input_frame = tk.Frame(self.window, bg='white')
            self.input_frame.pack(fill='x', padx=20, pady=10)

            button_container = tk.Frame(self.input_frame, bg='white')
            button_container.pack(side='right', fill='y')

            send_button = tk.Button(button_container, text="Enviar", command=self.send_message,
                                    bg='orange', fg='white', font=("Comic Sans MS", 12))
            send_button.pack(side='left', padx=5)

            mic_button = tk.Button(button_container, text="🎤", command=self.start_listening,
                                   bg='orange', fg='white', font=("Comic Sans MS", 12))
            mic_button.pack(side='left', padx=5)

            self.text_widget = tk.Text(self.input_frame, font=("Comic Sans MS", 13), wrap='word', height=1,
                                       spacing1=5, spacing3=5, padx=10, highlightthickness=0, bd=1, relief='solid')
            self.text_widget.pack(side='left', fill='x', expand=True)
            self.text_widget.bind("<Return>", lambda event: self.send_message())

            self.window.after(100, lambda: self.text_widget.focus_set())

        def update_response(self, new_text):
            if "Consultando..." in self.complete_text:
                self.complete_text = self.complete_text.replace("Consultando...", "")
            self.complete_text = new_text  # Se reemplaza completamente con la nueva respuesta

            self.response_text_widget.config(state="normal")
            self.response_text_widget.delete("1.0", tk.END)  # Se limpia antes de insertar el nuevo contenido

            self.insert_formatted_text(new_text)  # Usa la nueva función de formateo

            self.response_text_widget.config(state="disabled")
            self.response_text_widget.see("end")  # Auto-scroll al final


        def send_message(self):
            user_input = self.text_widget.get("1.0", tk.END).strip()
            if user_input:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.update_idletasks()  # Asegurar actualización inmediata
                self.update_response("Consultando...")  # Mostrar mensaje de carga
                self.window.after(100, lambda: fetch_response(user_input, self))  # Llamada diferida para evitar congelamiento

        def start_listening(self):
            self.update_response("\n[Escuchando...]\n")

    return CombinedWindow(root)



def fetch_response(user_text, response_window_instance):
    CombinedWindow = agent(user_text)  # Delegamos toda la lógica al agente

    # Asegurar que la respuesta no sea None
    if CombinedWindow is None:
        CombinedWindow = "Lo siento, no pude obtener una respuesta en este momento."

    # Actualizar la interfaz con la respuesta correcta
    response_window_instance.update_response(CombinedWindow)

    
def fetch_response(user_text, response_window_instance):
    CombinedWindow = agent(user_text)  # Delegamos toda la lógica al agente

    # Asegurar que la respuesta no sea None
    if CombinedWindow is None:
        CombinedWindow = "Lo siento, no pude obtener una respuesta en este momento."

    # Actualizar la interfaz con la respuesta correcta
    response_window_instance.update_response(CombinedWindow)


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
    response_window = show_combined_window(root)
    response_window.update_response(f"❌ : {message}")
        # Verifica si input_window existe antes de cerrarlo
    if input_window and input_window.winfo_exists():
        input_window.destroy()
    



# Función para enviar mensajes
def send_message(input_window, root, text_widget):
    user_text = text_widget.get("1.0", tk.END).strip()
    if user_text:
        response_window_instance = show_combined_window(root)
        response_window_instance.update_response("Consultando...")  # Mostrar mensaje de espera

        # Usar el agente para obtener una respuesta en un hilo separado
        threading.Thread(target=fetch_response, args=(user_text, response_window_instance)).start()
    input_window.destroy()


# Función para obtener la respuesta del agente
def fetch_response(user_text, response_window_instance):
    response = agent(user_text)  # Delegamos toda la lógica al agente

    # Asegurar que la respuesta no sea None
    if response is None:
        response = "Lo siento, no pude obtener una respuesta en este momento."

    # Actualizar la interfaz con la respuesta correcta
    response_window_instance.update_response(response)
    

# Función para ajustar la altura del cuadro de texto
def on_text_change(event, text_widget):
    content = text_widget.get("1.0", tk.END)
    lines = content.count('\n') + 1
    new_height = min(10, lines)  # Limitar a un máximo de 10 líneas visibles
    text_widget.config(height=new_height)


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
    muneco_label.bind("<Double-1>", lambda event: show_combined_window(root))
    muneco_label.bind("<ButtonRelease-3>", lambda event: show_animation_menu(event, root, muneco_label, fall_images, walk_images, climb_images, fly_image, muneco_photo))
    
    # Bind Ctrl+Q to close the application
    root.bind("<Control-q>", lambda event: [print("Bye Bye Camarada"), root.destroy()])
    

    return muneco_label, images

if __name__ == "__main__":
    root = tk.Tk()
    setup_gui(root)
    root.mainloop()