import requests
import json
import threading
from model import HistoryEntry, ApiKeyEntry, PythonDB
from alias_dic import predefined_answers

# Direct API Key
OPENROUTER_API_KEY = ApiKeyEntry.select_api_key()


# Historial de la conversación
conversation_history = []

def chat_with_bot(prompt):
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
                "temperature": 0.5
            })
        )

        print("Respuesta de la API recibida")

        if response.status_code == 401:
            print("Error de autenticación: Verifica tu clave de API.")
            return "Error de autenticación: Verifica tu clave de API."
        elif response.status_code != 200:
            print(f"Error en la respuesta de la API: {response.status_code} - {response.text}")
            return f"Error en la respuesta de la API: {response.status_code} - {response.text}"

        response_data = response.json()
        message_content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
        conversation_history.append({"role": "assistant", "content": message_content})

        return message_content
    except Exception as e:
        print(f"Error al llamar a la API de OpenRouter: {e}")
        return f"Error al llamar a la API de OpenRouter: {e}"

def agent(prompt):
    # Verificar si la pregunta está en las preguntas predeterminadas
    if prompt in predefined_answers:
        response = predefined_answers[prompt]
        if not HistoryEntry.get_by_prompt(prompt):
            HistoryEntry(prompt=prompt, response=response)
        return response

    # Buscar en la tabla de prompts predefinidos (PythonDB)
    try:
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            response = predefined_query.response
            if not HistoryEntry.get_by_prompt(prompt):
                HistoryEntry(prompt=prompt, response=response)
            return response
    except Exception as e:
        print(f"Error al consultar la python_db: {e}")

    # Buscar en la base de datos de historial
    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            return query.response
    except Exception as e:
        print(f"Error al consultar el historial: {e}")

    # Si no se encuentra en ningún lado, llamar a la API del modelo
    response = chat_with_bot(prompt)
    if not HistoryEntry.get_by_prompt(prompt):
        HistoryEntry(prompt=prompt, response=response)
    return response