import tkinter as tk
from tkinter import Toplevel, Text, Button, Frame, Label
from PIL import Image, ImageTk
from chatbot import chat_with_bot
import openai, json

class InteractiveDollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Muñeco Interactivo")
        self.root.configure(bg='white')
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.root.attributes("-transparentcolor", "white")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            self.muneco_image = Image.open('C:/Users/RuXx/Documents/StartUp/nobt/muneco.png')
            self.muneco_image = self.muneco_image.resize((200, 200), Image.LANCZOS)
            self.muneco_photo = ImageTk.PhotoImage(self.muneco_image)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            root.destroy()
            exit()

        self.muneco_label = tk.Label(root, image=self.muneco_photo, bg='white')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        initial_x = (screen_width // 2) - (200 // 2)
        initial_y = (screen_height // 2) - (200 // 2)
        self.muneco_label.place(x=initial_x, y=initial_y)

        self.root.after(100, self.apply_gravity)

        self.muneco_label.bind("<Button-1>", self.start_move)
        self.muneco_label.bind("<B1-Motion>", self.do_move)
        self.muneco_label.bind("<Double-1>", self.on_muneco_double_click)
        self.muneco_label.bind("<ButtonRelease-3>", self.on_right_click_release)

        self.root.bind("<Control-Key-1>", self.reset_api_key)

        # Agregar un botón para mostrar el historial
        self.history_button = Button(root, text="Mostrar Historial", command=self.show_history, bg='green', fg='white', font=("Arial", 14))
        self.history_button.pack(pady=10)

    def start_move(self, event):
        self.startX = event.x
        self.startY = event.y

    def do_move(self, event):
        x = self.muneco_label.winfo_x() + event.x - self.startX
        y = self.muneco_label.winfo_y() + event.y - self.startY

        if x < 0:
            x = 0
        elif x > self.root.winfo_width() - self.muneco_label.winfo_width():
            x = self.root.winfo_width() - self.muneco_label.winfo_width()

        if y < 0:
            y = 0
        elif y > self.root.winfo_height() - self.muneco_label.winfo_height():
            y = self.root.winfo_height() - self.muneco_label.winfo_height()

        self.muneco_label.place(x=x, y=y)

    def apply_gravity(self):
        x = self.muneco_label.winfo_x()
        y = self.muneco_label.winfo_y()
        if y < self.root.winfo_height() - self.muneco_label.winfo_height():
            self.muneco_label.place(x=x, y=y+10)
            self.root.after(50, self.apply_gravity)

    def on_right_click_release(self, event):
        self.apply_gravity()

    def on_muneco_double_click(self, event):
        self.input_window = Toplevel(self.root)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 100
        margin_bottom = 50
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = screen_height - window_height - margin_bottom
        self.input_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.input_window.configure(bg='white')

        self.frame = Frame(self.input_window, bg='white')
        self.frame.pack(pady=10, padx=10, expand=True, fill='both')

        self.send_button = Button(self.frame, text="Enviar", command=self.send_message, bg='blue', fg='white', font=("Arial", 14))
        self.send_button.pack(side='left', padx=10, pady=10, fill='y')

        self.text_widget = Text(self.frame, font=("Arial", 14), wrap='word', height=1)
        self.text_widget.pack(side='left', fill='both', expand=True)
        self.text_widget.bind("<KeyRelease>", self.on_text_change)
        self.text_widget.bind("<Return>", self.send_message)
        self.text_widget.bind("<Shift-Return>", lambda event: None)

        self.text_widget.focus_set()

    def send_message(self, event=None):
        user_text = self.text_widget.get("1.0", tk.END).strip()
        if user_text:
            chatbot_response = chat_with_bot(user_text)
            self.show_response(chatbot_response)
        self.input_window.destroy()

    def on_text_change(self, event):
        content = self.text_widget.get("1.0", tk.END)
        lines = content.count('\n') + 1
        new_height = min(10, lines)
        self.text_widget.config(height=new_height)

    def show_response(self, response_text):
        response_window = Toplevel(self.root)
        response_window.title("Respuesta del Chatbot")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 400
        window_height = 200
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        response_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        response_window.configure(bg='white')

        response_label = Label(response_window, text=response_text, bg='white', wraplength=350, font=("Arial", 14), justify="center")
        response_label.pack(pady=20, padx=20, expand=True, fill='both')

        close_button = Button(response_window, text="Cerrar", command=response_window.destroy, bg='red', fg='white', font=("Arial", 14))
        close_button.pack(pady=10)

    def reset_api_key(self, event=None):
        from config import reset_api_key
        global OPENAI_API_KEY
        OPENAI_API_KEY = reset_api_key()
        openai.api_key = OPENAI_API_KEY

    def show_history(self):
        history_window = Toplevel(self.root)
        history_window.title("Historial de Chat")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 400
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        history_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        history_window.configure(bg='white')


        try:
            with open("historic.json", "r", encoding="utf-8") as file:
                history_content_2 = file.read()

                texto_final = ""
                history_content_2 = json.loads(history_content_2)
                history_text = Text(history_window, font=("Arial", 12), wrap='word', bg='white')
                for item in history_content_2["converascion"]:
                    texto = f"""
                        question : {item["question"]}
                        respueta : {item["response"]}
                     """
                    # texto_final =  texto_final + texto

                    history_text.insert(tk.END, texto + '\n')
                    
                history_text.configure(state='disabled')
                history_text.pack(pady=10, padx=10, expand=True, fill='both')                        

                print(texto_final)
        except FileNotFoundError:
            history_content_2 = "No hay historial de chat disponible."

                     


        try:
            with open("chat_history.txt", "r", encoding="utf-8") as file:
                history_content = file.read()
        except FileNotFoundError:
            history_content = "No hay historial de chat disponible."

        # history_text = Text(history_window, font=("Arial", 12), wrap='word', bg='white')
        # history_text.insert(tk.END, history_content)
        # history_text.configure(state='disabled')
        # history_text.pack(pady=10, padx=10, expand=True, fill='both')

        close_button = Button(history_window, text="Cerrar", command=history_window.destroy, bg='red', fg='white', font=("Arial", 14))
        close_button.pack(pady=10)