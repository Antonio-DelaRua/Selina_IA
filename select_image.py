import tkinter as tk
from tkinter import Toplevel, Frame, Button
from PIL import Image, ImageTk

def select_image():
    selected_image = [None]

    def choose_image(image_path):
        selected_image[0] = image_path
        print(f"Imagen seleccionada: {image_path}")
        image_window.destroy()

    image_window = Toplevel(root)
    image_window.title("Selecciona una imagen")
    print("Ventana de selección de imagen creada.")
    
    frame = Frame(image_window, bg='white')
    frame.pack(pady=20, padx=20)

    try:
        # Cargar las imágenes
        muneco_image = Image.open('muneco.png')
        muneco_image = muneco_image.resize((200, 200), Image.LANCZOS)
        muneco_photo = ImageTk.PhotoImage(muneco_image)
        
        muneco1_image = Image.open('muneco1.png')
        muneco1_image = muneco1_image.resize((200, 200), Image.LANCZOS)
        muneco1_photo = ImageTk.PhotoImage(muneco1_image)
        
        # Botones para seleccionar las imágenes
        button1 = Button(frame, image=muneco_photo, command=lambda: choose_image('muneco.png'))
        button1.pack(side='left', padx=10)
        
        button2 = Button(frame, image=muneco1_photo, command=lambda: choose_image('muneco1.png'))
        button2.pack(side='right', padx=10)
        
        # Necesario para mantener una referencia a las imágenes
        button1.image = muneco_photo
        button2.image = muneco1_photo
        print("Imágenes cargadas y botones creados.")
    except Exception as e:
        print(f"Error al cargar las imágenes: {e}")
    
    image_window.mainloop()
    return selected_image[0]

def main():
    global root
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal durante la selección de la imagen
    print("Ventana principal creada y oculta.")

    selected_image = select_image()
    print(f"Imagen seleccionada: {selected_image}")
    if not selected_image:
        print("No se seleccionó ninguna imagen. Saliendo...")
        return

    root.deiconify()  # Mostrar la ventana principal después de seleccionar la imagen
    root.title("Visualizador de Imágenes")
    root.configure(bg='white')  # Fondo blanco para la ventana
    print("Ventana principal mostrada.")

    try:
        muneco_image = Image.open(selected_image)
        muneco_image = muneco_image.resize((200, 200), Image.LANCZOS)  # Redimensionar la imagen
        muneco_photo = ImageTk.PhotoImage(muneco_image)
        print(f"Imagen '{selected_image}' cargada y redimensionada.")
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return

    # Crear un label para el muñeco y colocar en el canvas
    muneco_label = tk.Label(root, image=muneco_photo, bg='white')
    muneco_label.image = muneco_photo  # Necesario para mantener una referencia a la imagen

    # Colocar el muñeco en el centro de la ventana
    muneco_label.pack(expand=True)
    print(f"Imagen '{selected_image}' colocada en la ventana principal.")

    root.mainloop()

if __name__ == "__main__":
    main()