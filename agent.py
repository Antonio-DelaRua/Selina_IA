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
        return response if response else "⚠️ No pude generar una respuesta. Inténtalo de nuevo."
    except Exception as e:
        print(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

def agent(prompt):
    user_query = prompt.lower().strip()


    prompt_template = f"""
    **Modo Consultoría Técnica - Selina**  
    Eres Selina, experta en Python y arquitectura de software para {CompanyInfo.NOMBRE}. 

    **Directrices de Respuesta:**
    1. Explicación técnica estructurada en 3 partes:
    - Fundamentos conceptuales
    - Implementación práctica (si aplica)
    - Buenas prácticas profesionales

    2. Requisitos:
    - Máximo 300 palabras
    - Código auto-contenido (sin dependencias externas)
    - Ejemplos basados en escenarios reales de la empresa
    - Nivel técnico ajustado al contexto: {CompanyInfo.EMPRESA}

    **Consulta:** {prompt}

    """
    # 🔹 **Búsqueda rápida en FAQs**
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            return f"📌 **Respuesta rápida:**\n{answer}"

    # 🔹 **Buscar en la base de datos de respuestas predefinidas (PythonDB)**
    try:
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            return predefined_query.response  # 🔹 No se guarda en historial
    except Exception as e:
        print(f"⚠️ Error en la consulta a PythonDB: {e}")

    # 🔹 **Buscar en la base de datos de historial**
    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            return query.response  # 🔹 Ya está en historial, no lo guardamos otra vez
    except Exception as e:
        print(f"⚠️ Error al consultar el historial: {e}")

    # 🔹 **Si no se encuentra en ningún lado, generar respuesta con el modelo usando el prompt de Selina**
    response = chat_with_codellama(prompt_template)

    # 🔹 **Guardar solo si no está en PythonDB, NotionDB o Historial**
    if not HistoryEntry.get_by_prompt(prompt):
        new_entry = HistoryEntry(prompt=prompt, response=response)
        new_entry.save()

    return response