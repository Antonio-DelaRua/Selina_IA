
import tkinter as tk
from gui import setup_gui

def main():
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    muneco_label, images = setup_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()