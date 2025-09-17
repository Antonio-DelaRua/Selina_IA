import webbrowser
import pyautogui as at
import time


def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
    time.sleep(10)  # Espera inicial para conexiones rápidas
    max_wait = 30   # Esperar hasta 30 segundos
    elapsed = 0

    while elapsed < max_wait:
        if "web.whatsapp.com" in at.getActiveWindow().title:
            break
        time.sleep(1)
        elapsed += 1

    if elapsed >= max_wait:
        print("⏳ Error: WhatsApp Web no se cargó a tiempo. Verifica tu conexión o sesión.")
        return

    time.sleep(5)  # Esperar a que cargue la conversación
    at.press('enter')