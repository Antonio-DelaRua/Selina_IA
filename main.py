import tkinter as tk
from gui import setup_gui


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