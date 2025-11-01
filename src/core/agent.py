import asyncio
import sys
import os
from langchain_ollama import OllamaLLM  # Para usar CodeLlama en local
from .model import HistoryEntry, PythonDB
from .info import CompanyInfo

# Fix import path for MCP manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp.manager import MCPManager


# 🚀 Cargar el modelo CodeLlama en local
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=900,
    repeat_penalty=1.2,
    num_gpu_layers=20,
)

# Inicializar MCP Manager para acciones del sistema
mcp_manager = MCPManager()

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

    # 🔄 1. Verificar si es una acción del sistema (prioridad máxima)
    system_keywords = [
        "abrir", "cerrar", "minimizar", "maximizar", "restaurar", "volumen", "brillo",
        "bloquear", "hibernar", "suspender", "apagar", "reiniciar", "cancelar apagado",
        "mute", "unmute", "subir volumen", "bajar volumen", "subir brillo", "bajar brillo"
    ]

    if any(keyword in user_query for keyword in system_keywords):
        try:
            # Inicializar MCP si no está inicializado
            await mcp_manager.initialize()

            # Parsear la solicitud del sistema
            request = parse_system_request(prompt)
            response = await mcp_manager.handle_request("system_control_mcp", request)

            if "error" not in response:
                # Guardar en historial
                if not HistoryEntry.get_by_prompt(prompt):
                    HistoryEntry(prompt=prompt, response=str(response)).save()
                return f"✅ Acción ejecutada: {response.get('message', 'Completada')}"
            else:
                return f"❌ Error en acción del sistema: {response['error']}"
        except Exception as e:
            return f"❌ Error al procesar acción del sistema: {str(e)}"

    # 🔄 2. Determinar dinámicamente si incluir contexto de la empresa
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

    # ✅ 3. Búsqueda en FAQs con coincidencia exacta
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

def parse_system_request(prompt):
    """Parsea una solicitud de usuario para convertirla en una petición MCP del sistema"""
    prompt_lower = prompt.lower().strip()

    # Abrir aplicaciones
    if "abrir" in prompt_lower:
        apps = {
            "calculadora": "calculator",
            "bloc de notas": "notepad",
            "explorador": "explorer",
            "cmd": "cmd",
            "paint": "paint",
            "google": "chrome",
            "chrome": "chrome"
        }
        for app_name, app_key in apps.items():
            if app_name in prompt_lower:
                return {"action": "open", "target": app_key}

    # Control de volumen
    if any(word in prompt_lower for word in ["volumen", "volume", "sonido"]):
        if "subir" in prompt_lower or "aumentar" in prompt_lower:
            value = 10  # default increment
            return {"action": "volume", "volume_action": "up", "value": value}
        elif "bajar" in prompt_lower or "disminuir" in prompt_lower:
            value = 10  # default decrement
            return {"action": "volume", "volume_action": "down", "value": value}
        elif "silenciar" in prompt_lower or "mute" in prompt_lower:
            return {"action": "volume", "volume_action": "mute"}
        elif "activar sonido" in prompt_lower or "unmute" in prompt_lower:
            return {"action": "volume", "volume_action": "unmute"}

    # Control de brillo
    if "brillo" in prompt_lower:
        if "subir" in prompt_lower or "aumentar" in prompt_lower:
            value = 10  # default increment
            return {"action": "brightness", "brightness_action": "up", "value": value}
        elif "bajar" in prompt_lower or "disminuir" in prompt_lower:
            value = 10  # default decrement
            return {"action": "brightness", "brightness_action": "down", "value": value}

    # Control de ventanas
    if any(word in prompt_lower for word in ["ventana", "window"]):
        if "minimizar" in prompt_lower or "minimize" in prompt_lower:
            return {"action": "window", "window_action": "minimize", "title": ""}
        elif "maximizar" in prompt_lower or "maximize" in prompt_lower:
            return {"action": "window", "window_action": "maximize", "title": ""}
        elif "restaurar" in prompt_lower or "restore" in prompt_lower:
            return {"action": "window", "window_action": "restore", "title": ""}
        elif "cerrar" in prompt_lower or "close" in prompt_lower:
            return {"action": "window", "window_action": "close", "title": ""}

    # Operaciones del sistema
    if any(word in prompt_lower for word in ["bloquear", "lock"]):
        return {"action": "system", "system_action": "lock"}
    elif any(word in prompt_lower for word in ["hibernar", "hibernate"]):
        return {"action": "system", "system_action": "hibernate"}
    elif any(word in prompt_lower for word in ["suspender", "sleep", "suspensión"]):
        return {"action": "system", "system_action": "sleep"}
    elif any(word in prompt_lower for word in ["apagar", "shutdown", "apagado"]):
        return {"action": "system", "system_action": "shutdown"}
    elif any(word in prompt_lower for word in ["reiniciar", "restart", "reinicio"]):
        return {"action": "system", "system_action": "restart"}
    elif "cancelar apagado" in prompt_lower or "cancel shutdown" in prompt_lower:
        return {"action": "system", "system_action": "cancel_shutdown"}

    # Default fallback
    return {"action": "unknown"}