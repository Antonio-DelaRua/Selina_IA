def apply_gravity(muneco_label, root, fall_images, muneco_photo):
    global animacion_id  # Variable global para rastrear la animación activa

    def fall_animation(index=1):  # Comenzar con la imagen fall_2
        global animacion_id  # Referencia a la variable global
        if index == 1:
            muneco_label.config(image=fall_images[1])
            x = muneco_label.winfo_x()
            y = muneco_label.winfo_y()
            if y < root.winfo_height() - muneco_label.winfo_height():
                muneco_label.place(x=x, y=y+20)  # Mover 20 píxeles hacia abajo
                animacion_id = root.after(40, fall_animation, 1)  # Esperar 40 ms y continuar
            else:
                animacion_id = root.after(100, fall_animation, 2)  # Cambiar a fall_3
        elif index == 2:
            muneco_label.config(image=fall_images[2])
            animacion_id = root.after(100, fall_animation, 0)  # Cambiar a fall_1
        else:
            muneco_label.config(image=muneco_photo)  # Cambiar a la imagen normal

    # Cancelar cualquier animación anterior antes de iniciar una nueva
    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)

    fall_animation()  # Iniciar animación
    return animacion_id  # Retornar el identificador

def move_to_edge(direction, muneco_label, root, walk_images, muneco_photo):
    global animacion_id  # Variable global para rastrear la animación actual

    def walk_animation(index=0):
        global animacion_id  # Usamos la variable global para almacenar el ID del after()
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()

        if direction == "left" and x > 0:
            muneco_label.config(image=walk_images[1])  # Set to walk_left_2
            muneco_label.place(x=x-5, y=y)  # Move left
            animacion_id = root.after(40, walk_animation, index + 1)  # Esperar 40ms y continuar
        elif direction == "right" and x < root.winfo_width() - muneco_label.winfo_width():
            muneco_label.config(image=walk_images[2])  # Set to walk_right_2
            muneco_label.place(x=x+5, y=y)  # Move right
            animacion_id = root.after(40, walk_animation, index + 1)  # Esperar 40ms y continuar
        else:
            muneco_label.config(image=muneco_photo)  # Restaurar imagen original

    # Cancelamos la animación anterior si hay una en curso
    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)

    walk_animation()  # Iniciar la animación
    return animacion_id  # Retornar el identificador



def climb_animation(muneco_label, root, climb_images, fly_image, muneco_photo):
    global animacion_id  # Variable global para rastrear la animación activa

    def climb(index=0):
        global animacion_id  # Referencia a la variable global
        x = root.winfo_width() - muneco_label.winfo_width()
        y = muneco_label.winfo_y()

        if y > 0:
            muneco_label.config(image=climb_images[index % len(climb_images)])
            muneco_label.place(x=x, y=y-6)  # Reducir la distancia de subida
            animacion_id = root.after(65, climb, index + 1)  # Aumentar la frecuencia de actualización
        else:
            muneco_label.config(image=fly_image)
            descend_zigzag()

    def descend_zigzag():
        global animacion_id  # Referencia a la variable global
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()

        if y < root.winfo_height() - muneco_label.winfo_height():
            new_x = x - 3  # Reducir la distancia de movimiento en X
            new_y = y + 3  # Reducir la distancia de movimiento en Y

            muneco_label.place(x=new_x, y=new_y)
            animacion_id = root.after(20, descend_zigzag)  # Aumentar la frecuencia de actualización
        else:
            muneco_label.config(image=muneco_photo)  # Restaurar imagen original

    # Cancelamos la animación anterior si existe
    if "animacion_id" in globals() and animacion_id:
        root.after_cancel(animacion_id)

    climb()  # Iniciar animación
    return animacion_id  # Retornar el identificador
