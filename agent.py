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

    # 🔄 1. Determinar dinámicamente si incluir contexto de la empresa
    contexto_empresa = ""
    if any(keyword in user_query for keyword in ["empresa", "compania", CompanyInfo.NAME.lower()]):
        contexto_empresa = f"\n\nContexto relevante:\n- Nombre: {CompanyInfo.NAME}\n- Sector: {CompanyInfo.INDUSTRY}\n- FAQs: {', '.join(CompanyInfo.FAQS.keys())}"

    prompt_template = f"""
        **Instrucciones clave:**
        1. Nunca menciones información de la empresa a menos que el usuario pregunte explícitamente
        2. Si necesitas hacer referencia a datos internos, usa solo las FAQs cuando haya coincidencia exacta
        3. Evita suposiciones sobre el contexto organizacional{contexto_empresa}

        **Consulta del usuario:** 
        {prompt}

        **Formato de respuesta requerido:**
        - Español con emojis relevantes ✨
        - Máximo 1 párrafo
        - Código breve si es útil (```python)
    """

    # ✅ 2. Búsqueda en FAQs con coincidencia exacta
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword.lower() == user_query:  # Coincidencia exacta
            return f"🔍 **Respuesta oficial:**\n{answer}"
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
