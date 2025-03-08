import pygame
import sys
import openai
import os
import tkinter as tk
from tkinter import ttk

# Inicializar Pygame
pygame.init()

# Configurar la API key de OpenAI
openai.api_key = "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"

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

def chat_with_bot(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error al llamar a la API de OpenAI: {e}")
        return "Lo siento, ocurrió un error al intentar comunicarme con el chatbot."

def draw_text_input_box(window, user_text, width, height):
    margin_bottom = 20
    input_box_width = width - 100
    input_box_height = 30
    input_box_x = (width - input_box_width) // 2
    input_box_y = height - input_box_height - margin_bottom
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
    pygame.draw.rect(window, WHITE, input_box)
    font = pygame.font.Font(None, 32)
    text_surface = font.render(user_text, True, BLACK)
    window.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    input_box.w = max(300, text_surface.get_width() + 10)
    return input_box

def draw_speech_bubble(window, text, muneco_rect):
    max_line_length = 30  # Máximo número de caracteres por línea
    font = pygame.font.Font(None, 24)
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Añadir la última línea

    bubble_width = 220
    bubble_height = len(lines) * 28 + 20  # Ajustar el tamaño del bocadillo según el número de líneas
    bubble_rect = pygame.Rect(muneco_rect.right + 10, muneco_rect.top, bubble_width, bubble_height)
    
    pygame.draw.rect(window, WHITE, bubble_rect, 0)
    
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        window.blit(text_surface, (bubble_rect.x + 10, bubble_rect.y + 10 + i * 28))

def run_pygame():
    width, height = 800, 600
    window = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.init()
    pygame.display.update()

    # Cargar el muñeco
    muneco_image = pygame.image.load('C:/Users/RuXx/Documents/SelinaIA/muneco.png')
    muneco_rect = muneco_image.get_rect()
    muneco_rect.topleft = (width // 2 - muneco_rect.width // 2, height // 2 - muneco_rect.height // 2)

    user_text = ''
    input_active = False
    chatbot_response = ''
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if muneco_rect.collidepoint(event.pos):
                    input_active = True
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        chatbot_response = chat_with_bot(user_text)
                        print("Chatbot dice:", chatbot_response)
                        user_text = ''
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        window.fill((0, 0, 0, 0))  # Transparente
        window.blit(muneco_image, muneco_rect.topleft)
        if input_active:
            draw_text_input_box(window, user_text, width, height)
        if chatbot_response:
            draw_speech_bubble(window, chatbot_response, muneco_rect)
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Muñeco Interactivo")
root.geometry("1900x800")
root.attributes("-transparentcolor", "black")

# Ejecutar Pygame en un hilo separado
import threading
thread = threading.Thread(target=run_pygame)
thread.start()

# Ejecutar el bucle principal de Tkinter
root.mainloop()