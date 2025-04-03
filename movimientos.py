# movimientos.py
def apply_gravity(muneco_label, root, fall_images, muneco_photo, muneco_active_image, window_abierta):
    global animacion_id

    def fall_animation(index=1):
        global animacion_id
        if index == 1:
            muneco_label.config(image=fall_images[1])
            x = muneco_label.winfo_x()
            y = muneco_label.winfo_y()
            if y < root.winfo_height() - muneco_label.winfo_height():
                muneco_label.place(x=x, y=y+20)
                animacion_id = root.after(40, fall_animation, 1)
            else:
                animacion_id = root.after(100, fall_animation, 2)
        elif index == 2:
            muneco_label.config(image=fall_images[2])
            animacion_id = root.after(100, fall_animation, 0)
        else:
            final_image = muneco_active_image if window_abierta else muneco_photo
            muneco_label.config(image=final_image)

    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)
    fall_animation()
    return animacion_id

def move_to_edge(direction, muneco_label, root, walk_images, muneco_photo, muneco_active_image, window_abierta):
    global animacion_id

    def walk_animation(index=0):
        global animacion_id
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()

        if direction == "left" and x > 0:
            muneco_label.config(image=walk_images[1])
            muneco_label.place(x=x-5, y=y)
            animacion_id = root.after(40, walk_animation, index + 1)
        elif direction == "right" and x < root.winfo_width() - muneco_label.winfo_width():
            muneco_label.config(image=walk_images[2])
            muneco_label.place(x=x+5, y=y)
            animacion_id = root.after(40, walk_animation, index + 1)
        else:
            final_image = muneco_active_image if window_abierta else muneco_photo
            muneco_label.config(image=final_image)

    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)
    walk_animation()
    return animacion_id

def climb_animation(muneco_label, root, climb_images, fly_image, muneco_photo, muneco_active_image, window_abierta):
    global animacion_id

    def climb(index=0):
        global animacion_id
        x = root.winfo_width() - muneco_label.winfo_width()
        y = muneco_label.winfo_y()

        if y > 0:
            muneco_label.config(image=climb_images[index % len(climb_images)])
            muneco_label.place(x=x, y=y-6)
            animacion_id = root.after(65, climb, index + 1)
        else:
            muneco_label.config(image=fly_image)
            descend_zigzag()

    def descend_zigzag():
        global animacion_id
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()

        if y < root.winfo_height() - muneco_label.winfo_height():
            new_x = x - 3
            new_y = y + 3
            muneco_label.place(x=new_x, y=new_y)
            animacion_id = root.after(20, descend_zigzag)
        else:
            final_image = muneco_active_image if window_abierta else muneco_photo
            muneco_label.config(image=final_image)

    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)
    climb()
    return animacion_id