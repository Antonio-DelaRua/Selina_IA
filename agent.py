import asyncio
from langchain_ollama import OllamaLLM  # Para usar CodeLlama en local
from model import HistoryEntry, PythonDB
from info import CompanyInfo
from last_history import *

# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=700,
    repeat_penalty=1.2,
    num_gpu_layers=20,
)

async def chat_with_codellama(prompt):
    """Llama a CodeLlama en local de forma asíncrona para evitar bloqueos."""
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, local_llm.invoke, prompt)
        return response or "⚠️ No pude generar una respuesta. Inténtalo de nuevo."
    except Exception as e:
        print(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

async def agent(prompt):
    user_query = prompt.lower().strip()

    # ✅ Si el usuario pide abrir el historial, lo abrimos y terminamos
    if user_query in ["abrir historial", "ver historial", "historial"]:
        return abrir_historial()

    prompt_template = f"""
    **Modo Consultoría Técnica - Selina**  
    Eres Selina, experta en Python y arquitectura de software para {CompanyInfo.NOMBRE}. 

    **Directrices Estrictas de Formato:**
    - Responder siempre en español, excepción: que se te indique lo contrario
    - Prohibido usar títulos como "Sección X" o "Tema Principal"
    - Usar solo emojis como separadores de contenido
    - Máximo 5 viñetas con emojis relevantes
    - Código en bloques con sintaxis específica

    **Ejemplo de Respuesta Esperada:**
    🧠 <descripción técnica clave>  
    🔧 <relación con arquitectura>  
    💡 <ventaja principal>  
    🚨 <consideración importante>  
    ```python
    <código mínimo enfocado>
    ```

    **Consulta:** {prompt}
    """

    # ✅ Búsqueda rápida en FAQs
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            respuesta = f"📌 **Respuesta rápida:**\n{answer}"
            guardar_en_txt(prompt, respuesta)  # Guardar en archivo
            return respuesta

    # ✅ Optimización: Consultas en base de datos (evita repeticiones)
    try:
        respuesta = PythonDB.get_by_prompt(prompt) or HistoryEntry.get_by_prompt(prompt)
        if respuesta:
            guardar_en_txt(prompt, respuesta.response)
            return respuesta.response
    except Exception as e:
        print(f"⚠️ Error en la consulta de base de datos: {e}")

    # 🔥 Generar respuesta con CodeLlama de forma asíncrona
    response = await chat_with_codellama(prompt_template)  

    # ✅ Guardar solo si no existe en historial
    if not HistoryEntry.get_by_prompt(prompt):
        HistoryEntry(prompt=prompt, response=response).save()

    # ✅ Guardar en archivo
    guardar_en_txt(prompt, response)

    return response
