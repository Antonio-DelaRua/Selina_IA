from model import HistoryEntry, PythonDB
from langchain_ollama import OllamaLLM  # Llamar a CodeLlama en local
from info import CompanyInfo
import os
import subprocess
from datetime import datetime


HISTORIAL_FILE = "historial_respuestas.txt"


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



def guardar_en_txt(prompt, response, max_entries=10):
    """
    Guarda la consulta y la respuesta en un archivo de texto, manteniendo solo las últimas 10 entradas,
    con mejor formato para mayor legibilidad.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_entrada = f"\n\n{'=' * 100}\n📅 Fecha: {timestamp}\n❓ Pregunta: {prompt}\n💡 Respuesta:\n{response}\n{'=' * 100}\n\n"

    # Leer historial existente si el archivo ya existe
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = f.read().strip().split("=" * 100 + "\n\n")  # Dividir correctamente

        # Mantener solo las últimas `max_entries - 1` respuestas y agregar la nueva
        historial = (historial[-(max_entries - 1):] if len(historial) >= max_entries else historial) + [nueva_entrada]
    else:
        historial = [nueva_entrada]

    # Sobrescribir el archivo con las últimas 10 respuestas
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(historial) + "\n")

def abrir_historial():
    """
    Abre el archivo historial_respuestas.txt con el editor de texto predeterminado.
    """
    if not os.path.exists(HISTORIAL_FILE):
        return "⚠️ No hay historial guardado aún."

    try:
        if os.name == "nt":  # Windows
            os.startfile(HISTORIAL_FILE)
        elif os.name == "posix":  # macOS/Linux
            subprocess.run(["xdg-open", HISTORIAL_FILE] if "linux" in os.sys.platform else ["open", HISTORIAL_FILE])
        return "📂 Historial abierto correctamente."
    except Exception as e:
        return f"❌ Error al abrir el historial: {e}"

def agent(prompt):
    user_query = prompt.lower().strip()

    # ✅ Si el usuario pide abrir el historial, lo abrimos y terminamos
    if user_query in ["abrir historial", "ver historial", "historial"]:
        return abrir_historial()

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

    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword in user_query:
            respuesta = f"📌 **Respuesta rápida:**\n{answer}"
            guardar_en_txt(prompt, respuesta)  # Guardar en archivo
            return respuesta

    try:
        predefined_query = PythonDB.get_by_prompt(prompt)
        if predefined_query:
            guardar_en_txt(prompt, predefined_query.response)  # Guardar en archivo
            return predefined_query.response
    except Exception as e:
        print(f"⚠️ Error en la consulta a PythonDB: {e}")

    try:
        query = HistoryEntry.get_by_prompt(prompt)
        if query:
            guardar_en_txt(prompt, query.response)  # Guardar en archivo
            return query.response
    except Exception as e:
        print(f"⚠️ Error al consultar el historial: {e}")

    response = chat_with_codellama(prompt_template)

    if not HistoryEntry.get_by_prompt(prompt):
        new_entry = HistoryEntry(prompt=prompt, response=response)
        new_entry.save()

    # Guardar la respuesta generada en el archivo (solo mantiene las últimas 10)
    guardar_en_txt(prompt, response)

    return response