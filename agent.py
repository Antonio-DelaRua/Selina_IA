import json
import aiohttp
from model import HistoryEntry, PythonDB
from fuzzywuzzy import process

# Clave API
OPENROUTER_API_KEY = "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"

# Historial de la conversación
conversation_history = []

async def chat_with_bot(prompt):
    try:
        async with aiohttp.ClientSession() as session:
            # Configura el payload correctamente
            payload = {
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [*conversation_history, {"role": "user", "content": prompt}],  # Agrega el prompt al historial
                "max_tokens": 950,
                "temperature": 0.7
            }
            
            async with session.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "<YOUR_SITE_URL>",
                    "X-Title": "<YOUR_SITE_NAME>",
                },
                json=payload  # ✅ Usa json= en lugar de data=json.dumps()
            ) as response:
                response_data = await response.json()
                message_content = response_data['choices'][0]['message']['content']
                conversation_history.append({"role": "assistant", "content": message_content})  # Actualiza historial
                return message_content
    except Exception as e:
        return f"Error: {str(e)}"

async def agent(prompt):
    try:
        # 1. Buscar en respuestas predefinidas
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            if not HistoryEntry.get_by_prompt(prompt):
                HistoryEntry(prompt=prompt, response=predefined_query.response)
            return predefined_query.response  # Retorna string
            
        # 2. Buscar en historial
        history_query = HistoryEntry.get_by_prompt(prompt)
        if history_query:
            return history_query.response  # Retorna string
            
        # 3. Llamar a la API (¡Añade await aquí!)
        api_response = await chat_with_bot(prompt)  # ✅ await es crítico
        HistoryEntry(prompt=prompt, response=api_response)
        return api_response  # Retorna string
        
    except Exception as e:
        return f"Error en el agente: {str(e)}"



