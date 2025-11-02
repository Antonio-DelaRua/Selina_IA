"""
Punto de entrada principal del sistema Selina IA
"""
import sys
import os

# Configurar el path para que sea un paquete
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import tkinter as tk
from ui.gui import setup_gui

def main():
    try:
        root = tk.Tk()
        setup_gui(root)

        root.mainloop()
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario")
    except Exception as e:
        print(f"Error durante la ejecución del programa: {e}")
    finally:
        print("Hasta pronto")

if __name__ == "__main__":
    main()