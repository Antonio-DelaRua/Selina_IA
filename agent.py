import requests
import json
from model import HistoryEntry, ApiKeyEntry

# Direct API Key
OPENROUTER_API_KEY = ApiKeyEntry.select_api_key()

# Lista de preguntas y respuestas predeterminadas
predefined_answers = {
    "¿Qué es Python?": "Python es un lenguaje de programación de alto nivel, interpretado, con una sintaxis muy clara y fácil de leer y escribir. Fue creado en el año 1991 por Guido van Rossum y su nombre se inspira en el grupo de comedia británico 'Monty Python's Flying Circus'.",
    "¿Qué es una API?": "Una API (Interfaz de Programación de Aplicaciones) es un conjunto de reglas y definiciones que permiten a las aplicaciones comunicarse entre sí.",
    "¿Quién es Guido van Rossum?": "Guido van Rossum es el creador del lenguaje de programación Python, y era un poco moñas."
}

# Función para consultar el modelo de IA
def query_ai_model(prompt):
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
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 950,
            "temperature": 0.5,
        })
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error en la respuesta de la API: {response.status_code} - {response.text}")

# Agente que busca en las preguntas predeterminadas, la base de datos y consulta al modelo de IA si no encuentra la información
def agent(prompt):
    # Verificar si la pregunta está en las preguntas predeterminadas
    if prompt in predefined_answers:
        return predefined_answers[prompt]

    # Buscar en la base de datos
    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            return query.response
        else:
            # Consultar el modelo de IA
            response = query_ai_model(prompt)
            history_entry = HistoryEntry(prompt=prompt, response=response)
            return response
    except Exception as e:
        print(f"Error al consultar el modelo de IA: {e}")
        return None

# Ejemplo de uso del agente
if __name__ == "__main__":
    prompt = "¿Qué es Python?"
    response = agent(prompt)
    print(f"Respuesta: {response}")

    prompt = "¿Qué es una API?"
    response = agent(prompt)
    print(f"Respuesta: {response}")

    prompt = "¿Quién es Guido van Rossum?"
    response = agent(prompt)
    print(f"Respuesta: {response}")