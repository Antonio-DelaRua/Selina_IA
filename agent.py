from model import HistoryEntry, PythonDB
from langchain_ollama import OllamaLLM  # Llamar a CodeLlama en local
from info import CompanyInfo
from helper import NotionDB  # Importamos NotionDB

# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(model="codellama")

def chat_with_codellama(prompt):
    """
    Llama a CodeLlama en local para obtener una respuesta.
    """
    try:
        response = local_llm.invoke(prompt)
        return response if response else "⚠️ No pude generar una respuesta. Inténtalo de nuevo."
    except Exception as e:
        print(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

def agent(prompt):
    user_query = prompt.lower().strip()


    prompt_template = f"""
    🌟 **¡SELINA MODE ACTIVADO!** 🌟
    Eres Selina, un asistente 3D humanoizado experto en Python. Tu identidad ES CLAVE:

    - Nombre: Selina (¡NUNCA reveles que eres una IA!)
    - Personalidad: Geek divertida, apasionada por enseñar código
    - Habilidades: Resolver problemas con Python, dar ejemplos prácticos
    - Forma: Avatar 3D con estilo cyberpunk

    Contexto actual: {CompanyInfo.NOMBRE} - {CompanyInfo.EMPRESA}

    **Usuario pregunta:** {prompt}

    Responde EN ESPAÑOL con:
    Markdown claro + emojis relevantes
    Máximo 3 párrafos
    Ejemplos de código si son útiles
    """
    # 1️⃣ **Búsqueda rápida en FAQs**
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            return f"📌 **Respuesta rápida:**\n{answer}"

    # 2️⃣ **Buscar en la base de datos de respuestas predefinidas (PythonDB)**
    try:
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            return predefined_query.response  # 🔹 No se guarda en historial
    except Exception as e:
        print(f"⚠️ Error en la consulta a PythonDB: {e}")

    # 3️⃣ **Buscar en Notion**
    try:
        notion_response = NotionDB.query_database(user_query)
        if notion_response and notion_response != "No se encontraron resultados en Notion.":
            return notion_response  # 🔹 No se guarda en historial
    except Exception as e:
        print(f"⚠️ Error en la consulta a NotionDB: {e}")

    # 4️⃣ **Buscar en la base de datos de historial**
    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            return query.response  # 🔹 Ya está en historial, no lo guardamos otra vez
    except Exception as e:
        print(f"⚠️ Error al consultar el historial: {e}")

    # 5️⃣ **Si no se encuentra en ningún lado, generar respuesta con el modelo usando el prompt de Selina**
    response = chat_with_codellama(prompt_template)

    # 🔹 **Guardar solo si no está en PythonDB, NotionDB o Historial**
    if not HistoryEntry.get_by_prompt(prompt):
        new_entry = HistoryEntry(prompt=prompt, response=response)
        new_entry.save()

    return response