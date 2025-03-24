from langchain_ollama import OllamaLLM  # Llamar a CodeLlama en local
from functools import lru_cache

cache_respuestas = {}

# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=700,
    repeat_penalty=1.2,
    num_gpu_layers=20,
)


def chat_with_codellama(prompt):
    """Llama a CodeLlama en local para obtener una respuesta optimizada."""
    try:
        return local_llm.invoke(prompt) or "⚠️ No pude generar una respuesta. Inténtalo de nuevo."
    except Exception as e:
        print(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"



def obtener_respuesta_cache(prompt):
    return cache_respuestas.get(prompt)

def guardar_respuesta_cache(prompt, respuesta):
    if len(cache_respuestas) > 50:  # Evita crecimiento infinito
        cache_respuestas.pop(next(iter(cache_respuestas)))  
    cache_respuestas[prompt] = respuesta

    