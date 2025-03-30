import asyncio
from langchain_ollama import OllamaLLM  # Para usar CodeLlama en local
from model import HistoryEntry, PythonDB
from info import CompanyInfo


# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=900,
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

    prompt_template = f"""

        Contexto actual: {CompanyInfo.NOMBRE} - {CompanyInfo.EMPRESA}

        **Usuario pregunta:** {prompt}

        Responde EN ESPAÑOL con:
        Markdown claro + emojis relevantes
        Máximo 1 párrafos
        Ejemplos de código si son útiles
    """

    # ✅ Búsqueda rápida en FAQs
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            respuesta = f"📌 **Respuesta rápida:**\n{answer}"
            return respuesta

    # ✅ Optimización: Consultas en base de datos (evita repeticiones)
    try:
        respuesta = PythonDB.get_by_prompt(prompt) or HistoryEntry.get_by_prompt(prompt)
        if respuesta:
            return respuesta.response
    except Exception as e:
        print(f"⚠️ Error en la consulta de base de datos: {e}")

    # 🔥 Generar respuesta con CodeLlama de forma asíncrona
    response = await chat_with_codellama(prompt_template)  

    # ✅ Guardar solo si no existe en historial
    if not HistoryEntry.get_by_prompt(prompt):
        HistoryEntry(prompt=prompt, response=response).save()


    return response
