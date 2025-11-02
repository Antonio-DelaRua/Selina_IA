"""
Agente principal con soporte MCP MEJORADO - refactorizado de agent.py
"""
import asyncio
import json
import logging
from langchain_ollama import OllamaLLM
from sqlalchemy import or_
import re
import os
import glob
import subprocess
import shutil

from config.settings import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_NUM_PREDICT, LLM_REPEAT_PENALTY,
    EMBEDDING_MODEL, EMB_DIM, INDEX_PATH, METADATA_PATH
)
from core.database import SessionLocal, PythonDB, History, HistoryEntry
from core.embeddings import vector_store, generate_embedding, semantic_search
from utils.info import CompanyInfo

logger = logging.getLogger(__name__)

# 🚀 LLM local
local_llm = OllamaLLM(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    num_predict=LLM_NUM_PREDICT,
    repeat_penalty=LLM_REPEAT_PENALTY,
)

class FilesystemTools:
    """Herramientas de filesystem integradas con MCP"""

    @staticmethod
    async def read_file(path: str) -> str:
        """Leer archivo de forma segura"""
        try:
            # Validar ruta segura
            if not os.path.exists(path):
                return f"❌ Archivo no encontrado: {path}"

            if not os.path.isfile(path):
                return f"❌ No es un archivo: {path}"

            # Limitar tamaño para seguridad
            if os.path.getsize(path) > 5 * 1024 * 1024:  # 5MB
                return "❌ Archivo demasiado grande (>5MB)"

            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Determinar tipo de archivo para formato
            file_ext = os.path.splitext(path)[1].lower()
            code_langs = {'.py': 'python', '.js': 'javascript', '.html': 'html', '.css': 'css', '.json': 'json'}
            lang = code_langs.get(file_ext, '')

            formatted_content = f"```{lang}\n{content[:3000]}\n```" if lang else f"```\n{content[:3000]}\n```"

            return f"## 📄 Contenido de `{path}`\n\n{formatted_content}"

        except PermissionError:
            return "❌ Permiso denegado para leer el archivo"
        except Exception as e:
            return f"❌ Error leyendo archivo: {str(e)}"

    @staticmethod
    async def list_directory(path: str) -> str:
        """Listar directorio de forma segura"""
        try:
            if not os.path.exists(path):
                return f"❌ Directorio no encontrado: {path}"

            if not os.path.isdir(path):
                return f"❌ No es un directorio: {path}"

            items = os.listdir(path)
            files = []
            directories = []

            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    size_str = f" ({size} bytes)" if size < 1024 else f" ({size/1024:.1f} KB)"
                    files.append(f"📄 {item}{size_str}")
                else:
                    directories.append(f"📁 {item}/")

            result = f"## 📂 Contenido de `{path}`\n\n"
            if directories:
                result += "### 📁 Directorios\n" + "\n".join(sorted(directories)) + "\n\n"
            if files:
                result += "### 📄 Archivos\n" + "\n".join(sorted(files))

            if not directories and not files:
                result += "📁 Directorio vacío"

            return result

        except PermissionError:
            return "❌ Permiso denegado para listar el directorio"
        except Exception as e:
            return f"❌ Error listando directorio: {str(e)}"

    @staticmethod
    async def search_files(query: str, path: str = ".") -> str:
        """Buscar archivos por nombre"""
        try:
            if not os.path.exists(path):
                return f"❌ Ruta no encontrada: {path}"

            # Búsqueda segura con glob
            search_path = os.path.join(path, f"*{query}*")
            matches = glob.glob(search_path)

            # Búsqueda recursiva opcional para resultados limitados
            if len(matches) < 5:
                recursive_path = os.path.join(path, "**", f"*{query}*")
                recursive_matches = glob.glob(recursive_path, recursive=True)
                matches.extend(recursive_matches[:10])  # Limitar resultados recursivos

            # Eliminar duplicados y limitar
            matches = list(set(matches))[:15]

            if not matches:
                return f"🔍 No se encontraron archivos con: '{query}' en `{path}`"

            result = f"## 🔍 Resultados para '{query}' en `{path}`\n\n"

            files = []
            dirs = []

            for match in matches:
                if os.path.isfile(match):
                    size = os.path.getsize(match)
                    size_str = f" ({size} bytes)" if size < 1024 else f" ({size/1024:.1f} KB)"
                    files.append(f"📄 {match}{size_str}")
                else:
                    dirs.append(f"📁 {match}/")

            if dirs:
                result += "### 📁 Directorios\n" + "\n".join(sorted(dirs)) + "\n\n"
            if files:
                result += "### 📄 Archivos\n" + "\n".join(sorted(files))

            return result

        except Exception as e:
            return f"❌ Error buscando archivos: {str(e)}"

    @staticmethod
    async def get_file_info(path: str) -> str:
        """Obtener información detallada de un archivo"""
        try:
            if not os.path.exists(path):
                return f"❌ Archivo no encontrado: {path}"

            stat = os.stat(path)
            file_info = {
                "Nombre": os.path.basename(path),
                "Ruta completa": os.path.abspath(path),
                "Tamaño": f"{stat.st_size} bytes",
                "Modificado": str(stat.st_mtime),
                "Es archivo": os.path.isfile(path),
                "Es directorio": os.path.isdir(path)
            }

            result = f"## 📊 Información de `{path}`\n\n"
            for key, value in file_info.items():
                result += f"**{key}:** {value}\n"

            return result

        except Exception as e:
            return f"❌ Error obteniendo información: {str(e)}"

    @staticmethod
    async def move_file(source: str, destination: str) -> str:
        """Mover o renombrar archivos/directorios de forma segura"""
        try:
            # Validar que el archivo origen existe
            if not os.path.exists(source):
                return f"❌ Archivo origen no encontrado: {source}"

            # Validar permisos
            if not os.access(source, os.R_OK):
                return f"❌ Sin permisos de lectura para: {source}"

            # Crear directorio destino si no existe
            dest_dir = os.path.dirname(destination)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            # Verificar si el destino ya existe
            if os.path.exists(destination):
                return f"❌ El destino ya existe: {destination}"

            # Mover el archivo
            shutil.move(source, destination)

            # Verificar que se movió correctamente
            if os.path.exists(destination) and not os.path.exists(source):
                return f"✅ **Archivo movido exitosamente**\n\n**Origen:** `{source}`\n**Destino:** `{destination}`"
            else:
                return "❌ Error: No se pudo completar el movimiento"

        except PermissionError:
            return "❌ Permiso denegado para mover el archivo"
        except Exception as e:
            return f"❌ Error moviendo archivo: {str(e)}"

class MCPDatabaseServer:
    """Servidor MCP que PRIORIZA la base de datos local + Filesystem"""

    def __init__(self, llm):
        self.llm = llm
        self.tools = self._setup_tools()
        self.session_factory = SessionLocal
        self.fs_tools = FilesystemTools()

    def _setup_tools(self):
        return {
            # 🗄️ Herramientas existentes de base de datos
            "code_analysis": {
                "name": "code_analysis",
                "description": "Analizar código Python usando base de datos local",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Código a analizar"}
                    },
                    "required": ["code"]
                }
            },
            "explain_concept": {
                "name": "explain_concept",
                "description": "Explicar concepto usando base de datos local",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept": {"type": "string", "description": "Concepto a explicar"}
                    },
                    "required": ["concept"]
                }
            },
            "debug_code": {
                "name": "debug_code",
                "description": "Debuggear código usando base de datos local",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Código con error"},
                        "error": {"type": "string", "description": "Mensaje de error"}
                    },
                    "required": ["code"]
                }
            },
            "search_knowledge": {
                "name": "search_knowledge",
                "description": "Buscar en toda la base de conocimientos",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Término a buscar"}
                    },
                    "required": ["query"]
                }
            },

            # 📅 HERRAMIENTAS DE CALENDARIO
            "calendar_query": {
                "name": "calendar_query",
                "description": "Consultar tareas del calendario",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Consulta sobre tareas (ej: 'tareas hoy', 'tareas mañana')"}
                    },
                    "required": ["query"]
                }
            },

            # 📁 NUEVAS herramientas de filesystem
            "move_file": {
                "name": "move_file",
                "description": "Mover o renombrar archivos y directorios",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "Ruta del archivo/directorio origen"},
                        "destination": {"type": "string", "description": "Ruta del archivo/directorio destino"}
                    },
                    "required": ["source", "destination"]
                }
            },
            "read_file": {
                "name": "read_file",
                "description": "Leer contenido de archivos locales",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Ruta completa del archivo"}
                    },
                    "required": ["path"]
                }
            },
            "list_directory": {
                "name": "list_directory",
                "description": "Listar archivos y directorios",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Ruta del directorio (default: actual)"}
                    },
                    "required": ["path"]
                }
            },
            "search_files": {
                "name": "search_files",
                "description": "Buscar archivos por nombre",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Término de búsqueda"},
                        "path": {"type": "string", "description": "Directorio donde buscar", "default": "."}
                    },
                    "required": ["query"]
                }
            },
            "file_info": {
                "name": "file_info",
                "description": "Obtener información detallada de archivo/directorio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Ruta del archivo/directorio"}
                    },
                    "required": ["path"]
                }
            }
        }

    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Ejecutar herramienta MCP - PRIORIZANDO BASE DE DATOS + FILESYSTEM"""
        try:
            # 1️⃣ PRIMERO: Herramientas de Filesystem (rápidas)
            if tool_name in ["read_file", "list_directory", "search_files", "file_info", "move_file"]:
                fs_response = await self._call_filesystem_tool(tool_name, arguments)
                return fs_response

            # 2️⃣ SEGUNDO: Buscar en base de datos
            db_response = await self._search_in_database(tool_name, arguments)
            if db_response:
                return f"## 🗄️ **Desde Base de Datos**\n\n{db_response}"

            # 3️⃣ TERCERO: Si no hay resultados, usar LLM
            llm_response = await self._call_llm_tool(tool_name, arguments)
            return f"## 🤖 **Generado por IA**\n\n{llm_response}"

        except Exception as e:
            logger.error(f"Error en herramienta MCP {tool_name}: {e}")
            return f"❌ Error ejecutando {tool_name}: {str(e)}"

    async def _call_filesystem_tool(self, tool_name: str, arguments: dict) -> str:
        """Ejecutar herramientas de filesystem"""
        try:
            if tool_name == "read_file":
                return await self.fs_tools.read_file(arguments["path"])
            elif tool_name == "list_directory":
                path = arguments.get("path", ".")
                return await self.fs_tools.list_directory(path)
            elif tool_name == "search_files":
                path = arguments.get("path", ".")
                return await self.fs_tools.search_files(arguments["query"], path)
            elif tool_name == "file_info":
                return await self.fs_tools.get_file_info(arguments["path"])
            elif tool_name == "move_file":
                return await self.fs_tools.move_file(arguments["source"], arguments["destination"])
            else:
                return f"❌ Herramienta de filesystem desconocida: {tool_name}"
        except Exception as e:
            logger.error(f"Error en herramienta filesystem {tool_name}: {e}")
            return f"❌ Error en filesystem: {str(e)}"

    async def _search_in_database(self, tool_name: str, arguments: dict) -> str:
        """Buscar en la base de datos SQLite antes de usar LLM"""
        try:
            # Primero verificar si es consulta de calendario
            if tool_name == "calendar_query":
                from .database import Task
                query = arguments.get("query", "").lower()

                if "tareas hoy" in query or "qué tareas tengo hoy" in query:
                    tasks = Task.get_tasks_for_today()
                    if tasks:
                        response = "**Tus tareas para hoy:**\n\n"
                        for task in tasks:
                            status = "✅" if task.completed else "⏳"
                            time_str = f" ({task.time})" if task.time else ""
                            response += f"{status} {task.title}{time_str}\n"
                        return response
                    else:
                        return "No tienes tareas programadas para hoy."

                elif "tareas mañana" in query:
                    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                    tasks = Task.get_tasks_for_date(tomorrow)
                    if tasks:
                        response = "**Tus tareas para mañana:**\n\n"
                        for task in tasks:
                            status = "✅" if task.completed else "⏳"
                            time_str = f" ({task.time})" if task.time else ""
                            response += f"{status} {task.title}{time_str}\n"
                        return response
                    else:
                        return "No tienes tareas programadas para mañana."

            with self.session_factory() as session:
                if tool_name == "code_analysis":
                    code = arguments.get("code", "").strip()
                    if not code:
                        return None

                    # Buscar código similar en la base de datos
                    results = session.query(PythonDB).filter(
                        or_(
                            PythonDB.prompt.ilike(f"%{code}%"),
                            PythonDB.response.ilike(f"%{code}%")
                        )
                    ).limit(3).all()

                    if results:
                        response = "**Análisis encontrado en base de datos:**\n\n"
                        for i, result in enumerate(results, 1):
                            response += f"**{i}. {result.prompt[:100]}...**\n"
                            response += f"{result.response}\n\n"
                        return response

                elif tool_name == "explain_concept":
                    concept = arguments.get("concept", "").lower().strip()

                    # Buscar concepto en FAQs, PythonDB e History
                    # 1. Buscar en FAQs
                    faq_results = []
                    for keyword, answer in CompanyInfo.FAQS.items():
                        if concept in keyword.lower():
                            faq_results.append(f"**FAQ:** {keyword}\n{answer}")

                    # 2. Buscar en PythonDB
                    db_results = session.query(PythonDB).filter(
                        or_(
                            PythonDB.prompt.ilike(f"%{concept}%"),
                            PythonDB.response.ilike(f"%{concept}%")
                        )
                    ).limit(2).all()

                    # 3. Buscar en History
                    history_results = session.query(History).filter(
                        or_(
                            History.prompt.ilike(f"%{concept}%"),
                            History.response.ilike(f"%{concept}%")
                        )
                    ).limit(2).all()

                    all_results = faq_results + [
                        f"**Base de Datos:** {result.prompt}\n{result.response}"
                        for result in db_results
                    ] + [
                        f"**Historial:** {result.prompt}\n{result.response}"
                        for result in history_results
                    ]

                    if all_results:
                        response = "**Explicaciones encontradas:**\n\n"
                        for i, result in enumerate(all_results[:3], 1):
                            response += f"{result}\n\n"
                        return response

                elif tool_name == "debug_code":
                    code = arguments.get("code", "").strip()
                    error = arguments.get("error", "").strip()

                    search_terms = [code]
                    if error:
                        search_terms.append(error)

                    results = []
                    for term in search_terms:
                        if term:
                            # Buscar en PythonDB
                            db_matches = session.query(PythonDB).filter(
                                or_(
                                    PythonDB.prompt.ilike(f"%{term}%"),
                                    PythonDB.response.ilike(f"%{term}%")
                                )
                            ).limit(2).all()

                            # Buscar en History
                            history_matches = session.query(History).filter(
                                or_(
                                    History.prompt.ilike(f"%{term}%"),
                                    History.response.ilike(f"%{term}%")
                                )
                            ).limit(2).all()

                            results.extend(db_matches + history_matches)

                    if results:
                        response = "**Soluciones de debugging encontradas:**\n\n"
                        for i, result in enumerate(results[:3], 1):
                            response += f"**{i}. {result.prompt[:100]}...**\n"
                            response += f"{result.response}\n\n"
                        return response

                elif tool_name == "search_knowledge":
                    query = arguments.get("query", "").strip()

                    # Búsqueda completa en toda la base de conocimientos
                    all_results = []

                    # Buscar en FAQs
                    for keyword, answer in CompanyInfo.FAQS.items():
                        if query.lower() in keyword.lower():
                            all_results.append(f"📚 **FAQ:** {keyword}\n{answer}")

                    # Buscar en PythonDB
                    db_results = session.query(PythonDB).filter(
                        or_(
                            PythonDB.prompt.ilike(f"%{query}%"),
                            PythonDB.response.ilike(f"%{query}%")
                        )
                    ).limit(3).all()

                    # Buscar en History
                    history_results = session.query(History).filter(
                        or_(
                            History.prompt.ilike(f"%{query}%"),
                            History.response.ilike(f"%{query}%")
                        )
                    ).limit(3).all()

                    all_results.extend([
                        f"💾 **Base de Datos:** {result.prompt}\n{result.response}"
                        for result in db_results
                    ] + [
                        f"📝 **Historial:** {result.prompt}\n{result.response}"
                        for result in history_results
                    ])

                    if all_results:
                        response = f"## 🔍 **Resultados para: '{query}'**\n\n"
                        for i, result in enumerate(all_results[:5], 1):
                            response += f"{i}. {result}\n\n"
                        return response

            return None

        except Exception as e:
            logger.error(f"Error buscando en base de datos: {e}")
            return None

    async def _call_llm_tool(self, tool_name: str, arguments: dict) -> str:
        """Usar LLM solo si no hay resultados en BD"""
        try:
            if tool_name == "code_analysis":
                code = arguments.get("code", "")
                prompt = f"""
                Analiza BREVEMENTE este código Python (máximo 100 palabras):

                ```python
                {code}
                ```

                Responde en español con:
                • Función principal
                • Una mejora sugerida
                • Posible error

                Sé CONCISO.
                """

            elif tool_name == "explain_concept":
                concept = arguments.get("concept", "")
                prompt = f"""
                Explica BREVEMENTE '{concept}' en programación (máximo 80 palabras):

                • Definición simple
                • Ejemplo práctico en Python
                • Caso de uso común

                Sé CONCISO y usa español.
                """

            elif tool_name == "debug_code":
                code = arguments.get("code", "")
                error = arguments.get("error", "")
                prompt = f"""
                Debug rápido (máximo 80 palabras):

                Código: ```python
                {code}
                ```

                {"Error: " + error if error else "Problema: no funciona"}

                • Causa probable
                • Solución simple
                • Código corregido breve

                Sé CONCISO.
                """

            elif tool_name == "search_knowledge":
                query = arguments.get("query", "")
                prompt = f"""
                Responde BREVEMENTE sobre '{query}' en programación (máximo 100 palabras):

                • Concepto clave
                • Ejemplo práctico
                • Uso común

                Sé CONCISO.
                """

            # LLM con timeout corto
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, self.llm.invoke, prompt),
                timeout=30.0
            )

            # Guardar en la base de datos para futuras consultas
            await self._save_to_database(tool_name, arguments, response)

            return response.strip() if response else "No pude generar una respuesta."

        except asyncio.TimeoutError:
            return "⏰ Tiempo agotado. Intenta con una consulta más específica."
        except Exception as e:
            logger.error(f"Error llamando LLM: {e}")
            return f"Error: {str(e)}"

    async def _save_to_database(self, tool_name: str, arguments: dict, response: str):
        """Guardar la respuesta en la base de datos para futuras consultas"""
        try:
            with self.session_factory() as session:
                if tool_name == "code_analysis":
                    prompt = f"Análisis de código: {arguments.get('code', '')[:200]}"
                    entry = PythonDB(prompt=prompt, response=response)

                elif tool_name == "explain_concept":
                    prompt = f"Explicar concepto: {arguments.get('concept', '')}"
                    entry = PythonDB(prompt=prompt, response=response)

                elif tool_name == "debug_code":
                    code = arguments.get('code', '')[:150]
                    error = arguments.get('error', '')
                    prompt = f"Debug: {code} - Error: {error}" if error else f"Debug: {code}"
                    entry = PythonDB(prompt=prompt, response=response)

                elif tool_name == "search_knowledge":
                    prompt = f"Búsqueda: {arguments.get('query', '')}"
                    entry = PythonDB(prompt=prompt, response=response)

                session.add(entry)
                session.commit()
                logger.info("✅ Respuesta guardada en base de datos")

        except Exception as e:
            logger.error(f"Error guardando en base de datos: {e}")

    def list_tools(self) -> list:
        """Listar herramientas disponibles"""
        return list(self.tools.values())

async def parse_natural_command(command: str) -> dict:
    """Parsear comandos naturales en español a formato MCP"""
    command = command.lower().strip()

    # 📁 FILESYSTEM COMMANDS
    if command.startswith("listar"):
        # "listar ." o "listar /ruta"
        parts = command.split()
        if len(parts) >= 2:
            path = parts[1] if len(parts) > 1 else "."
            return {"tool": "list_directory", "arguments": {"path": path}}
        return {"tool": "list_directory", "arguments": {"path": "."}}

    elif command.startswith("leer"):
        # "leer archivo.py"
        parts = command.split()
        if len(parts) >= 2:
            path = " ".join(parts[1:])  # Permitir espacios en nombres de archivo
            return {"tool": "read_file", "arguments": {"path": path}}

    elif command.startswith("buscar"):
        # "buscar 'palabra' en /ruta" o "buscar palabra"
        parts = command.split()
        if len(parts) >= 2:
            # Extraer término de búsqueda (puede estar entre comillas)
            query = parts[1]
            if query.startswith('"') and query.endswith('"'):
                query = query[1:-1]
            elif query.startswith("'") and query.endswith("'"):
                query = query[1:-1]

            # Verificar si hay "en ruta"
            path = "."
            if "en" in parts and len(parts) > parts.index("en") + 1:
                path = parts[parts.index("en") + 1]

            return {"tool": "search_files", "arguments": {"query": query, "path": path}}

    elif command.startswith("info"):
        # "info archivo.txt"
        parts = command.split()
        if len(parts) >= 2:
            path = " ".join(parts[1:])
            return {"tool": "file_info", "arguments": {"path": path}}

    elif command.startswith("mover"):
        # "mover origen.txt destino.txt"
        parts = command.split()
        if len(parts) >= 3:
            source = parts[1]
            destination = " ".join(parts[2:])
            return {"tool": "move_file", "arguments": {"source": source, "destination": destination}}

    # 📅 CALENDAR COMMANDS
    elif command.startswith("calendario") or command.startswith("tareas"):
        # "calendario tareas hoy" o "tareas mañana"
        query = command.replace("calendario", "").replace("tareas", "").strip()
        if not query:
            query = "tareas hoy"
        return {"tool": "calendar_query", "arguments": {"query": query}}

    # 🗄️ DATABASE COMMANDS
    elif command.startswith("analizar"):
        # "analizar def funcion(): ..."
        code = command.replace("analizar", "").strip()
        return {"tool": "code_analysis", "arguments": {"code": code}}

    elif command.startswith("explicar"):
        # "explicar listas"
        concept = command.replace("explicar", "").strip()
        return {"tool": "explain_concept", "arguments": {"concept": concept}}

    elif command.startswith("debug"):
        # "debug def funcion(): ..." o "debug error: mensaje"
        content = command.replace("debug", "").strip()
        if ":" in content:
            code, error = content.split(":", 1)
            return {"tool": "debug_code", "arguments": {"code": code.strip(), "error": error.strip()}}
        else:
            return {"tool": "debug_code", "arguments": {"code": content}}

    # 🔍 GENERAL SEARCH
    elif command.startswith("conocimiento") or command.startswith("saber"):
        # "conocimiento python" o "saber sobre listas"
        query = command.replace("conocimiento", "").replace("saber", "").replace("sobre", "").strip()
        return {"tool": "search_knowledge", "arguments": {"query": query}}

    # No reconocido
    return None
def convert_single_quotes_to_double(json_str):
    """Convierte comillas simples a dobles para JSON válido"""
    pattern = r"'([^']*)'"

    def replace_quotes(match):
        content = match.group(1)
        content = content.replace('"', '\\"')
        return f'"{content}"'

    result = re.sub(pattern, replace_quotes, json_str)
    return result

async def handle_mcp_command(command: str) -> str:
    """Manejar comandos MCP - AHORA CON FILESYSTEM Y COMANDOS NATURALES"""
    try:
        if command == "help" or command == "tools":
            tools = mcp_server.list_tools()

            # Separar herramientas por categoría
            db_tools = [t for t in tools if t['name'] in ['code_analysis', 'explain_concept', 'debug_code', 'search_knowledge']]
            fs_tools = [t for t in tools if t['name'] in ['read_file', 'list_directory', 'search_files', 'file_info', 'move_file']]
            calendar_tools = [t for t in tools if t['name'] in ['calendar_query']]

            db_list = "\n".join([f"- **{tool['name']}**: {tool['description']}" for tool in db_tools])
            fs_list = "\n".join([f"- **{tool['name']}**: {tool['description']}" for tool in fs_tools])

            return f"""
## 🛠️ **Herramientas MCP Disponibles**

### 📅 **Calendario**
{chr(10).join([f"- **{tool['name']}**: {tool['description']}" for tool in calendar_tools])}

### ️ **Base de Datos**
{db_list}

### 📁 **Filesystem**
{fs_list}

**📝 Sintaxis Antigua (JSON):**
- `/mcp {{"tool": "list_directory", "arguments": {{"path": "."}}}}`

**🆕 Sintaxis Nueva (Natural):**
- `/mcp listar .`
- `/mcp leer archivo.py`
- `/mcp buscar "palabra" en /ruta`
- `/mcp info archivo.txt`
- `/mcp mover origen.txt destino.txt`
- `/mcp calendario tareas hoy`

**📋 Comandos Naturales Disponibles:**
- `listar [ruta]` → list_directory
- `leer [archivo]` → read_file
- `buscar "término" [en ruta]` → search_files
- `info [archivo]` → file_info
- `mover [origen] [destino]` → move_file
- `calendario [consulta]` → calendar_query
- `analizar [código]` → code_analysis
- `explicar [concepto]` → explain_concept
- `debug [código]` → debug_code
- `buscar [término]` → search_knowledge
"""

        # 🆕 NUEVO: Parsear comandos naturales en español
        parsed_command = await parse_natural_command(command.strip())
        if parsed_command:
            tool_name = parsed_command["tool"]
            arguments = parsed_command["arguments"]

            # Ejecutar herramienta MEJORADA
            response = await asyncio.wait_for(
                mcp_server.call_tool(tool_name, arguments),
                timeout=45.0
            )
            return response

        # Fallback: Sintaxis JSON antigua
        # Convertir comillas simples a dobles
        command_clean = command.strip()
        if "'" in command_clean and '"' not in command_clean:
            command_clean = convert_single_quotes_to_double(command_clean)

        try:
            data = json.loads(command_clean)
            tool_name = data.get("tool")
            arguments = data.get("arguments", {})

            if not tool_name:
                return "❌ Error: Falta el nombre de la herramienta"

            # Ejecutar herramienta MEJORADA
            response = await asyncio.wait_for(
                mcp_server.call_tool(tool_name, arguments),
                timeout=45.0
            )
            return response

        except json.JSONDecodeError as e:
            return f"❌ Error en formato. Usa sintaxis natural o JSON válido.\n\nEjemplos:\n- `/mcp listar .`\n- `/mcp {{\"tool\": \"list_directory\", \"arguments\": {{\"path\": \".\"}}}}`"

    except Exception as e:
        logger.error(f"Error en comando MCP: {e}")
        return f"❌ Error: {str(e)}"

async def chat_with_codellama(prompt):
    """Llama al modelo CodeLlama local de forma asíncrona"""
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, local_llm.invoke, prompt)
        return response.strip() if response else "⚠️ No pude generar una respuesta."
    except Exception as e:
        logger.error(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

def search_in_faqs(user_query):
    """Búsqueda más inteligente en FAQs"""
    user_query_lower = user_query.lower().strip()

    # Coincidencia exacta
    for keyword, answer in CompanyInfo.FAQS.items():
        if keyword.lower() == user_query_lower:
            return answer

    # Búsqueda por palabras clave
    query_words = set(user_query_lower.split())
    for keyword, answer in CompanyInfo.FAQS.items():
        keyword_words = set(keyword.lower().split())
        if query_words.intersection(keyword_words):
            return answer

    return None

async def agent(prompt):
    """Agente principal con soporte MCP MEJORADO"""
    if not prompt or not prompt.strip():
        return "❌ Por favor, ingresa una pregunta válida."

    user_query = prompt.strip()
    logger.info(f"🔍 Procesando consulta: {user_query}")

    # 1️⃣ Detectar si es un comando MCP (AHORA CON FILESYSTEM)
    if user_query.startswith("/mcp "):
        return await handle_mcp_command(user_query[5:])

    # 2️⃣ Buscar en FAQs (rápido)
    faq_response = search_in_faqs(user_query)
    if faq_response:
        logger.info("✅ Respuesta encontrada en FAQs")
        return f"🔍 **Respuesta oficial:**\n{faq_response}"

    # 3️⃣ Buscar semánticamente en embeddings locales (rápido)
    semantic_response = semantic_search(user_query)
    if semantic_response:
        logger.info("✅ Respuesta encontrada por búsqueda semántica")
        return f"📘 **Respuesta encontrada en base de conocimientos:**\n{semantic_response}"

    # 4️⃣ Buscar en base de datos exacta (rápido)
    try:
        with SessionLocal() as session:
            db_response = session.query(PythonDB).filter(
                PythonDB.prompt.ilike(f"%{user_query}%")
            ).first()

            if db_response:
                logger.info("✅ Respuesta encontrada en base de datos exacta")
                return f"📚 **Respuesta encontrada en base de datos:**\n{db_response.response}"
    except Exception as e:
        logger.error(f"⚠️ Error en consulta SQL: {e}")

    # 5️⃣ Si no hay coincidencia, usar LLM (LENTO - solo como último recurso)
    logger.info("🤖 Generando respuesta con LLM (puede tardar)")
    prompt_template = f"""
Responde BREVEMENTE en español (máximo 150 palabras):

Pregunta: {user_query}

Respuesta concisa:
"""

    try:
        # Timeout para el LLM lento también
        response = await asyncio.wait_for(
            chat_with_codellama(prompt_template),
            timeout=120.0  # 2 minutos máximo
        )

        # Guardar en historial (no bloquear con esto)
        try:
            embedding = generate_embedding(user_query)
            history_entry = HistoryEntry(prompt=user_query, response=response)
            history_entry.set_embedding(embedding)
            history_entry.save()

            # También guardar en PythonDB para MCP
            with SessionLocal() as session:
                python_entry = PythonDB(prompt=user_query, response=response)
                python_entry.set_embedding(embedding)
                session.add(python_entry)
                session.commit()

            vector_store.add_to_index(embedding, user_query, response, "history")
        except Exception as e:
            logger.error(f"Error guardando en historial: {e}")

        return f"💡 **Respuesta:**\n{response}"

    except asyncio.TimeoutError:
        return "⏰ **El modelo está tardando demasiado.**\n\n💡 **Sugerencias:**\n• Reformula tu pregunta\n• Usa `/mcp help` para herramientas rápidas\n• Pregunta cosas más específicas"
    except Exception as e:
        logger.error(f"❌ Error en el agente: {e}")
        return f"❌ Error: {str(e)}"

# Inicializar MCP Server MEJORADO con Filesystem
mcp_server = MCPDatabaseServer(local_llm)