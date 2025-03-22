import requests
import json
import threading
from model import HistoryEntry, PythonDB
from alias_dic import predefined_answers
from fuzzywuzzy import process

# Direct API Key
OPENROUTER_API_KEY = "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"

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

def find_closest_match(prompt):
    match, score = process.extractOne(prompt, predefined_answers.keys())
    if score > 80:  # Umbral de similitud
        return match
    return None

def agent(prompt):
    # Buscar el prompt más cercano en las respuestas predefinidas
    closest_match = find_closest_match(prompt)
    if closest_match:
        response = predefined_answers[closest_match]
        if not HistoryEntry.get_by_prompt(closest_match):
            HistoryEntry(prompt=closest_match, response=response)
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