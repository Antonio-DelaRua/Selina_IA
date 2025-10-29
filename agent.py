import asyncio
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM
from sqlalchemy.orm import sessionmaker
from model import History, HistoryEntry, PythonDB, engine
from info import CompanyInfo
import logging
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🚀 Modelo de embeddings local
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
EMB_DIM = 384
INDEX_PATH = "vector_index.faiss"
METADATA_PATH = "vector_metadata.json"

# 🚀 LLM local (CodeLlama) - SOLO para respuestas complejas
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=900,
    repeat_penalty=1.2,
    num_gpu_layers=20,
)

# 🚀 LLM RÁPIDO para herramientas MCP
fast_llm = OllamaLLM(
    model="qwen2.5:0.5b",  # Modelo más pequeño y rápido
    temperature=0.1,
    num_predict=700,  # Respuestas más cortas
    repeat_penalty=1.1,
    num_gpu_layers=10,
)

class MCPServer:
    """Servidor MCP integrado en la aplicación - VERSIÓN RÁPIDA"""
    
    def __init__(self, fast_llm):
        self.fast_llm = fast_llm
        self.tools = self._setup_tools()
    
    def _setup_tools(self):
        return {
            "code_analysis": {
                "name": "code_analysis",
                "description": "Analizar y explicar código Python",
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
                "description": "Explicar concepto de programación",
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
                "description": "Ayudar a debuggear código",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "code": {"type": "string", "description": "Código con error"},
                        "error": {"type": "string", "description": "Mensaje de error"}
                    },
                    "required": ["code"]
                }
            }
        }
    
    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Ejecutar una herramienta MCP - VERSIÓN RÁPIDA"""
        try:
            if tool_name == "code_analysis":
                code = arguments.get("code", "")
                # Respuesta rápida predefinida para código simple
                if len(code) < 100:
                    quick_response = self._quick_code_analysis(code)
                    if quick_response:
                        return quick_response
                
                prompt = f"""
                Analiza BREVEMENTE este código Python (máximo 150 palabras):

                ```python
                {code}
                ```

                Responde en español con:
                • Función: ¿qué hace?
                • Mejora: una sugerencia
                • Error: posible problema

                Sé CONCISO.
                """
                response = await self._call_fast_llm(prompt)
                return f"## 🔍 Análisis Rápido\n\n{response}"
                
            elif tool_name == "explain_concept":
                concept = arguments.get("concept", "")
                # Respuesta rápida para conceptos comunes
                quick_explanation = self._quick_concept_explanation(concept)
                if quick_explanation:
                    return quick_explanation
                
                prompt = f"""
                Explica BREVEMENTE '{concept}' en programación (máximo 100 palabras):

                • Definición simple
                • Ejemplo práctico
                • Caso de uso

                Sé CONCISO y usa español.
                """
                response = await self._call_fast_llm(prompt)
                return f"## 📖 Explicación: {concept}\n\n{response}"
                
            elif tool_name == "debug_code":
                code = arguments.get("code", "")
                error = arguments.get("error", "")
                
                prompt = f"""
                Debug rápido (máximo 100 palabras):

                Código: ```python
                {code}
                ```

                {"Error: " + error if error else "Problema: no funciona"}

                • Causa probable
                • Solución simple
                • Código corregido breve

                Sé CONCISO.
                """
                response = await self._call_fast_llm(prompt)
                return f"## 🐛 Debug Rápido\n\n{response}"
                
            else:
                return f"❌ Herramienta desconocida: {tool_name}"
                
        except Exception as e:
            logger.error(f"Error en herramienta MCP {tool_name}: {e}")
            return f"❌ Error ejecutando {tool_name}: {str(e)}"
    
    def _quick_code_analysis(self, code: str) -> str:
        """Análisis rápido predefinido para código común"""
        code_lower = code.lower()
        
        # Patrones comunes
        if "print(" in code_lower and "hello" in code_lower:
            return "## 🔍 Análisis Rápido\n\n**Función:** Muestra 'hello' en pantalla\n**Mejora:** Usar f-strings para variables\n**Error:** Ninguno, es código básico"
        
        if "def " in code_lower and "return" in code_lower:
            return "## 🔍 Análisis Rápido\n\n**Función:** Define una función que retorna valor\n**Mejora:** Añadir docstring y validaciones\n**Error:** Posible falta de manejo de casos edge"
        
        if "for " in code_lower and " in " in code_lower:
            return "## 🔍 Análisis Rápido\n\n**Función:** Bucle que itera sobre elementos\n**Mejora:** Usar list comprehension si es simple\n**Error:** Posible iteración sobre tipo incorrecto"
            
        return None
    
    def _quick_concept_explanation(self, concept: str) -> str:
        """Explicación rápida predefinida para conceptos comunes"""
        concept_lower = concept.lower()
        
        explanations = {
            "lista": "## 📖 Listas en Python\n\n• **Definición:** Colección ordenada y mutable de elementos\n• **Ejemplo:** `mi_lista = [1, 2, 'hola']`\n• **Uso:** Para almacenar múltiples valores relacionados",
            "función": "## 📖 Funciones en Python\n\n• **Definición:** Bloque de código reutilizable\n• **Ejemplo:** `def suma(a, b): return a + b`\n• **Uso:** Organizar código y evitar repetición",
            "variable": "## 📖 Variables en Python\n\n• **Definición:** Contenedor para almacenar datos\n• **Ejemplo:** `edad = 25`\n• **Uso:** Guardar y manipular valores",
            "bucle": "## 📖 Bucles en Python\n\n• **Definición:** Repetir código múltiples veces\n• **Ejemplo:** `for i in range(5): print(i)`\n• **Uso:** Procesar listas o repetir acciones",
            "condicional": "## 📖 Condicionales en Python\n\n• **Definición:** Ejecutar código según condición\n• **Ejemplo:** `if edad >= 18: print('Mayor')`\n• **Uso:** Tomar decisiones en el programa"
        }
        
        for key, explanation in explanations.items():
            if key in concept_lower:
                return explanation
                
        return None
    
    async def _call_fast_llm(self, prompt: str) -> str:
        """Llamar al LLM RÁPIDO con timeout"""
        try:
            # Timeout de 30 segundos máximo
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, self.fast_llm.invoke, prompt),
                timeout=30.0
            )
            return response.strip() if response else "⚠️ Respuesta demasiado larga, intenta con menos código."
        except asyncio.TimeoutError:
            return "⏰ Tiempo agotado. El código es muy complejo o el modelo está lento. Intenta con menos código."
        except Exception as e:
            logger.error(f"Error llamando LLM rápido: {e}")
            return f"Error temporal: {str(e)}"
    
    def list_tools(self) -> list:
        """Listar herramientas disponibles"""
        return list(self.tools.values())

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        
    def load_embeddings_from_db(self):
        """Cargar embeddings guardados en PythonDB + History"""
        Session = sessionmaker(bind=engine)
        with Session() as session:
            python_entries = session.query(PythonDB).filter(PythonDB.embedding.isnot(None)).all()
            history_entries = session.query(History).filter(History.embedding.isnot(None)).all()
            
            all_entries = []
            for entry in python_entries + history_entries:
                try:
                    emb = np.array(json.loads(entry.embedding), dtype=np.float32)
                    all_entries.append({
                        'embedding': emb,
                        'response': entry.response,
                        'prompt': entry.prompt,
                        'source': 'python_db' if isinstance(entry, PythonDB) else 'history',
                        'id': entry.id
                    })
                except json.JSONDecodeError as e:
                    logger.warning(f"Error cargando embedding de {type(entry).__name__}: {e}")
                except Exception as e:
                    logger.error(f"Error procesando entrada de {type(entry).__name__}: {e}")
            
            return all_entries

    def build_or_load_faiss_index(self):
        """Construye o carga el índice FAISS desde disco"""
        try:
            self.index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, 'r') as f:
                self.metadata = json.load(f)
            logger.info(f"✅ Índice FAISS cargado desde disco con {len(self.metadata)} vectores.")
            return True
        except Exception as e:
            logger.info("⚙️ No se encontró índice. Creando uno nuevo...")
            return self._build_new_index()

    def _build_new_index(self):
        """Construye un nuevo índice FAISS"""
        try:
            self.index = faiss.IndexFlatIP(EMB_DIM)
            data = self.load_embeddings_from_db()
            
            if data:
                vectors = np.vstack([d['embedding'] for d in data])
                faiss.normalize_L2(vectors)
                self.index.add(vectors)
                self.metadata = data
                
                faiss.write_index(self.index, INDEX_PATH)
                with open(METADATA_PATH, 'w') as f:
                    json.dump(data, f, default=str)
                    
                logger.info(f"✅ Índice FAISS construido con {len(data)} vectores.")
            else:
                logger.info("⚠️ No hay embeddings aún en la base de datos.")
                
            return True
        except Exception as e:
            logger.error(f"❌ Error construyendo índice: {e}")
            return False

    def add_to_index(self, embedding, prompt, response, source="history"):
        """Agrega un nuevo embedding al índice"""
        try:
            if self.index is None:
                self._build_new_index()
                
            # Normalizar y agregar el embedding
            emb_array = np.array([embedding], dtype=np.float32)
            faiss.normalize_L2(emb_array)
            self.index.add(emb_array)
            
            # Agregar metadata
            new_entry = {
                'embedding': embedding.tolist(),
                'response': response,
                'prompt': prompt,
                'source': source,
                'id': len(self.metadata)
            }
            self.metadata.append(new_entry)
            
            # Guardar en disco
            faiss.write_index(self.index, INDEX_PATH)
            with open(METADATA_PATH, 'w') as f:
                json.dump(self.metadata, f, default=str)
                
            logger.info("✅ Nuevo vector agregado al índice.")
            return True
        except Exception as e:
            logger.error(f"❌ Error agregando al índice: {e}")
            return False

# Inicializar vector store
vector_store = VectorStore()
vector_store.build_or_load_faiss_index()

# Inicializar MCP Server CON LLM RÁPIDO
mcp_server = MCPServer(fast_llm)

def generate_embedding(text):
    """Generar embedding numpy para un texto"""
    return embedding_model.encode(text, normalize_embeddings=True).astype(np.float32)

async def chat_with_codellama(prompt):
    """Llama al modelo CodeLlama local de forma asíncrona"""
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, local_llm.invoke, prompt)
        return response.strip() if response else "⚠️ No pude generar una respuesta."
    except Exception as e:
        logger.error(f"❌ Error al llamar a CodeLlama: {e}")
        return f"Error al llamar a CodeLlama: {e}"

def semantic_search(query_text, top_k=5, threshold=0.7):
    """Busca respuestas similares usando embeddings y FAISS"""
    if vector_store.index is None or vector_store.index.ntotal == 0:
        return None

    try:
        query_emb = generate_embedding(query_text)
        query_emb = np.array([query_emb])
        faiss.normalize_L2(query_emb)
        
        # Buscar los top_k más similares
        D, I = vector_store.index.search(query_emb, top_k)

        candidates = []
        for dist, idx in zip(D[0], I[0]):
            if 0 <= idx < len(vector_store.metadata) and dist >= threshold:
                metadata = vector_store.metadata[idx]
                candidates.append({
                    'response': metadata['response'],
                    'similarity': float(dist),
                    'source': metadata['source']
                })

        if not candidates:
            return None

        # Retornar la respuesta más similar
        best_candidate = max(candidates, key=lambda x: x['similarity'])
        return best_candidate['response']
        
    except Exception as e:
        logger.error(f"❌ Error en búsqueda semántica: {e}")
        return None

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
    """Manejar comandos MCP desde el chat - VERSIÓN RÁPIDA"""
    try:
        if command == "help" or command == "tools":
            tools = mcp_server.list_tools()
            tools_list = "\n".join([f"- **{tool['name']}**: {tool['description']}" for tool in tools])
            return f"""
## 🛠️ **Herramientas MCP Disponibles** ⚡

{tools_list}

**Uso:** `/mcp <comando_json>`

**📝 Ejemplos RÁPIDOS:**

**1. Análisis de código:**
`/mcp {{"tool": "code_analysis", "arguments": {{"code": "print('hola')"}}}}`

**2. Explicar concepto:**
`/mcp {{"tool": "explain_concept", "arguments": {{"concept": "listas"}}}}`

**3. Debuggear:**
`/mcp {{"tool": "debug_code", "arguments": {{"code": "x=1/0", "error": "Division by zero"}}}}`

💡 **Las herramientas MCP son RÁPIDAS** (max 30 segundos)
            """
        
        # Convertir comillas simples a dobles para JSON válido
        command_clean = command.strip()
        
        # Si el comando usa comillas simples, convertirlas a dobles
        if "'" in command_clean and '"' not in command_clean:
            command_clean = convert_single_quotes_to_double(command_clean)
        
        try:
            # Parsear el JSON
            data = json.loads(command_clean)
            
            tool_name = data.get("tool")
            arguments = data.get("arguments", {})
            
            if not tool_name:
                return "❌ Error: Falta el nombre de la herramienta"
            
            # Ejecutar la herramienta CON TIMEOUT
            response = await asyncio.wait_for(
                mcp_server.call_tool(tool_name, arguments),
                timeout=35.0  # Timeout de 35 segundos
            )
            return response
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")
            
            # Intentar parseo con regex como fallback
            try:
                tool_match = re.search(r'["\']tool["\']\s*:\s*["\']([^"\']*)["\']', command)
                if tool_match:
                    tool_name = tool_match.group(1)
                    
                    arguments = {}
                    code_match = re.search(r'["\']code["\']\s*:\s*["\']([^"\']*)["\']', command)
                    if code_match:
                        arguments['code'] = code_match.group(1)
                    
                    concept_match = re.search(r'["\']concept["\']\s*:\s*["\']([^"\']*)["\']', command)
                    if concept_match:
                        arguments['concept'] = concept_match.group(1)
                    
                    error_match = re.search(r'["\']error["\']\s*:\s*["\']([^"\']*)["\']', command)
                    if error_match:
                        arguments['error'] = error_match.group(1)
                    
                    if arguments:
                        response = await asyncio.wait_for(
                            mcp_server.call_tool(tool_name, arguments),
                            timeout=35.0
                        )
                        return response
                        
            except Exception as parse_error:
                logger.error(f"Error en parseo alternativo: {parse_error}")
            
            return f"""
❌ **Error en el formato JSON**

**Usa este formato:** `/mcp {{"tool": "nombre", "arguments": {{"param": "valor"}}}}`

**Ejemplo:** `/mcp {{"tool": "code_analysis", "arguments": {{"code": "print('hola')"}}}}`
"""
        except asyncio.TimeoutError:
            return "⏰ **¡Demasiado lento!** ⚡\n\nLa herramienta tardó demasiado. Intenta con:\n• Código más corto\n• Conceptos más simples\n• Menos texto"
        
    except Exception as e:
        logger.error(f"Error en comando MCP: {e}")
        return f"❌ Error: {str(e)}"

async def agent(prompt):
    """Agente principal con soporte MCP"""
    if not prompt or not prompt.strip():
        return "❌ Por favor, ingresa una pregunta válida."

    user_query = prompt.strip()
    logger.info(f"🔍 Procesando consulta: {user_query}")

    # 1️⃣ Detectar si es un comando MCP (RÁPIDO)
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
        db_response = PythonDB.get_by_prompt(user_query) or HistoryEntry.get_by_prompt(user_query)
        if db_response:
            logger.info("✅ Respuesta encontrada en base de datos exacta")
            return f"📚 **Respuesta encontrada en base de datos:**\n{db_response.response}"
    except Exception as e:
        logger.error(f"⚠️ Error en consulta SQL: {e} - Consulta: {user_query}")

    # 5️⃣ Si no hay coincidencia, usar CodeLlama (LENTO - solo como último recurso)
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
            vector_store.add_to_index(embedding, user_query, response, "history")
        except Exception as e:
            logger.error(f"Error guardando en historial: {e}")
        
        return f"💡 **Respuesta:**\n{response}"
        
    except asyncio.TimeoutError:
        return "⏰ **El modelo está tardando demasiado.**\n\n💡 **Sugerencias:**\n• Reformula tu pregunta\n• Usa `/mcp help` para herramientas rápidas\n• Pregunta cosas más específicas"
    except Exception as e:
        logger.error(f"❌ Error en el agente: {e}")
        return f"❌ Error: {str(e)}"