def apply_gravity(muneco_label, root):
    x = muneco_label.winfo_x()
    y = muneco_label.winfo_y()
    if y < root.winfo_height() - muneco_label.winfo_height():
        muneco_label.place(x=x, y=y+10)
        root.after(50, apply_gravity, muneco_label, root)