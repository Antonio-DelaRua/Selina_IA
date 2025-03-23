import json
from model import HistoryEntry, PythonDB
from langchain_ollama import OllamaLLM  # Llamar a CodeLlama en local
from info import CompanyInfo

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

    for pattern, response in corporate_keywords.items():
        if any(kw in user_query for kw in pattern.split("|")):
            return response

    # 4️⃣ **Buscar en la base de datos de respuestas predefinidas**
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
    response = chat_with_codellama(prompt)
    if not HistoryEntry.get_by_prompt(prompt):
        HistoryEntry(prompt=prompt, response=response)
    return response
