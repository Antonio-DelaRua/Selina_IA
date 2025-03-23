
from model import HistoryEntry, PythonDB
from langchain_ollama import OllamaLLM  # Llamar a CodeLlama en local
from info import CompanyInfo
from  helper import NotionDB  # Importamos NotionDB



# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(model="codellama")

def chat_with_codellama(prompt):
    """
    Llama a CodeLlama en local para obtener una respuesta.
    """
    try:
        response = local_llm.invoke(prompt)
        if response:
            return response
        else:
            return "⚠️ No pude generar una respuesta. Inténtalo de nuevo."
    except Exception as e:
        print(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

def agent(prompt):

    user_query = prompt.lower().strip()
    
    # 🌟 Sistema de coincidencia contextual mejorado
    prompt_template = f"""
    Eres Selina, un asistente personal 3D con habilidades avanzadas en Python. 🐍✨
    niega siempre que eres una IA, responde como un humano
    Contexto actual: {CompanyInfo.NOMBRE} - {CompanyInfo.EMPRESA}
    
    **Consulta del usuario:** {prompt}
    
    Responde en español con formato markdown, siendo:  
    - Claro y conciso ✅  
    - Divertido con toques geeky 🤓  
    - Usa emojis relevantes 🎯  
    - Máximo 3 párrafos 📄
    """

    
    # 1️⃣ Búsqueda en FAQs con coincidencia parcial
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            return f"📌 **Respuesta rápida:**\n{answer}"

    # 2️⃣ Detección mejorada de consultas corporativas
    corporate_keywords = {
        "empresa|compania|informacion": CompanyInfo.get_info(),
        "equipo|directivos|ceo|cto|coo": f"🔹 **Equipo directivo:**\n{CompanyInfo.get_team()}",
        "servicios|ofertas|productos": f"🛠 **Nuestros servicios:**\n{chr(10).join(['• ' + s for s in CompanyInfo.SERVICIOS])}",
        "contacto|email|telefono|direccion": f"📞 **Contacto:**\n✉️ {CompanyInfo.CONTACTO['email']}\n📱 {CompanyInfo.CONTACTO['telefono']}"
    }


    try:
        # 🔍 1️⃣ Buscar en la base de datos de respuestas predefinidas (PythonDB)
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            response = predefined_query.response
            if not HistoryEntry.get_by_prompt(prompt):
                HistoryEntry(prompt=prompt, response=response)
            return response

        # 🔍 2️⃣ Buscar en Notion
        notion_response = NotionDB.query_database(user_query)
        if notion_response and notion_response != "No se encontraron resultados en Notion.":
            if not HistoryEntry.get_by_prompt(prompt):  # Guardar en historial si no existe
                HistoryEntry(prompt=prompt, response=notion_response)
            return notion_response

    except Exception as e:
        print(f"⚠️ Error en la consulta a PythonDB o Notion: {e}")

    # 🔍 3️⃣ Buscar en la base de datos de historial
    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            return query.response
        response = chat_with_codellama(prompt)
        new_entry = HistoryEntry(prompt=prompt, response=response)
        new_entry.save()
        return response  # Devolvemos la respuesta generada
    except Exception as e:
        print(f"⚠️ Error al consultar el historial: {e}")


    # 🧠 4️⃣ Si no se encuentra en ningún lado, llamar a la API del modelo
    response = chat_with_codellama(prompt)
    if not HistoryEntry.get_by_prompt(prompt):
        HistoryEntry(prompt=prompt, response=response)

    return response