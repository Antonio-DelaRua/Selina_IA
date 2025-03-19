import requests
import json
import threading
from model import HistoryEntry, ApiKeyEntry, engine


OPENROUTER_API_KEY = ApiKeyEntry.select_api_key()

# Historial de la conversación
conversation_history = []

def chat_with_bot(prompt, update_callback, finish_callback):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Opcional. URL del sitio para rankings en openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>",  # Opcional. Título del sitio para rankings en openrouter.ai.
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": conversation_history,
                "max_tokens": 950,
                "temperature": 0.5,
                "stream": True  # Habilitar la transmisión de respuestas
            }),
            stream=True
        )

        #print("Respuesta de la API recibida")

        if response.status_code == 401:
            print("Error de autenticación: Verifica tu clave de API.")
            update_callback("Error de autenticación: Verifica tu clave de API.")
            finish_callback()
            return
        elif response.status_code != 200:
            print(f"Error en la respuesta de la API: {response.status_code} - {response.text}")
            update_callback(f"Error en la respuesta de la API: {response.status_code} - {response.text}")
            finish_callback()
            return

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                #print(f"Línea recibida: {decoded_line}")  # Depuración
                if decoded_line.startswith("data: "):
                    decoded_line = decoded_line[6:]
                    if decoded_line != "[DONE]":
                        response_data = json.loads(decoded_line)
                        choice = response_data.get('choices', [{}])[0]
                        message_content = choice.get('delta', {}).get('content', '')
                        update_callback(message_content)
        finish_callback()  # Indicar que el stream ha finalizado
    except Exception as e:
        print(f"Error al llamar a la API de OpenRouter: {e}")
        update_callback(f"Error al llamar a la API de OpenRouter: {e}")
        finish_callback()

