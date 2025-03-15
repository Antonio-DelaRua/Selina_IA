def apply_gravity(muneco_label, root, fall_images, muneco_photo):
    def fall_animation(index=1):  # Comenzar con la imagen fall_2
        if index == 1:
            muneco_label.config(image=fall_images[1])
            x = muneco_label.winfo_x()
            y = muneco_label.winfo_y()
            if y < root.winfo_height() - muneco_label.winfo_height():
                muneco_label.place(x=x, y=y+20)  # Mover 20 píxeles hacia abajo
                root.after(40, fall_animation, 1)  # Esperar 40 ms
            else:
                root.after(100, fall_animation, 2)  # Cambiar a la imagen fall_3
        elif index == 2:
            muneco_label.config(image=fall_images[2])
            root.after(100, fall_animation, 0)  # Cambiar a la imagen fall_1
        else:
            muneco_label.config(image=fall_images[0])
            # Puedes agregar un after aquí para que el muñeco siga cayendo

    fall_animation()

def move_to_edge(direction, muneco_label, root, walk_images, muneco_photo):
    def walk_animation(index=0):
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()
        if direction == "left" and x > 0:
            muneco_label.config(image=walk_images[1])  # Set to walk_left_2
            muneco_label.place(x=x-5, y=y)  # Move 10 pixels
            root.after(40, walk_animation, index + 1)  # Reduce delay to 40 milliseconds
        elif direction == "right" and x < root.winfo_width() - muneco_label.winfo_width():
            muneco_label.config(image=walk_images[2])  # Set to walk_left_3
            muneco_label.place(x=x+5, y=y)  # Move 10 pixels
            root.after(40, walk_animation, index + 1)  # Reduce delay to 40 milliseconds
        else:
            # Cuando se llega al final, cambia a la imagen original del muñeco
            muneco_label.config(image=muneco_photo)  # Cambia a la imagen original

    walk_animation()

def climb_animation(muneco_label, root, climb_images, fly_image, muneco_photo):
    def climb(index=0):
        x = root.winfo_width() - muneco_label.winfo_width()
        y = muneco_label.winfo_y()
        if y > 0:
            muneco_label.config(image=climb_images[index % len(climb_images)])
            muneco_label.place(x=x, y=y-3)  # Reducir la distancia de subida
            root.after(20, climb, index + 1)  # Aumentar la frecuencia de actualización
        else:
            # When reaching the top, change to flying image and start descending in a zigzag pattern
            muneco_label.config(image=fly_image)
            descend_zigzag()

    def descend_zigzag():
        x = muneco_label.winfo_x()
        y = muneco_label.winfo_y()

        # Move diagonally downwards from top-right to bottom-left
        if y < root.winfo_height() - muneco_label.winfo_height():
            new_x = x - 3  # Reducir la distancia de movimiento en X
            new_y = y + 3  # Reducir la distancia de movimiento en Y

            muneco_label.place(x=new_x, y=new_y)
            root.after(20, descend_zigzag)  # Aumentar la frecuencia de actualización
        else:
            # When reaching the bottom, set the final image
            muneco_label.config(image=muneco_photo)

    climb()
