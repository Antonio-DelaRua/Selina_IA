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
from sqlalchemy import or_

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🚀 Modelo de embeddings local
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
EMB_DIM = 384
INDEX_PATH = "vector_index.faiss"
METADATA_PATH = "vector_metadata.json"

# 🚀 LLM local
local_llm = OllamaLLM(
    model="qwen2.5:0.5b",
    temperature=0.5,
    num_predict=500,
    repeat_penalty=1.2,
)

class MCPDatabaseServer:
    """Servidor MCP que PRIORIZA la base de datos local"""
    
    def __init__(self, llm):
        self.llm = llm
        self.tools = self._setup_tools()
        self.session_factory = sessionmaker(bind=engine)
    
    def _setup_tools(self):
        return {
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
            }
        }
    
    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Ejecutar herramienta MCP - PRIORIZANDO BASE DE DATOS"""
        try:
            # 1️⃣ PRIMERO buscar en base de datos
            db_response = await self._search_in_database(tool_name, arguments)
            if db_response:
                return f"## 🗄️ **Desde Base de Datos**\n\n{db_response}"
            
            # 2️⃣ SI NO HAY RESULTADOS, usar LLM
            llm_response = await self._call_llm_tool(tool_name, arguments)
            return f"## 🤖 **Generado por IA**\n\n{llm_response}"
                
        except Exception as e:
            logger.error(f"Error en herramienta MCP {tool_name}: {e}")
            return f"❌ Error ejecutando {tool_name}: {str(e)}"
    
    async def _search_in_database(self, tool_name: str, arguments: dict) -> str:
        """Buscar en la base de datos SQLite antes de usar LLM"""
        try:
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

# Inicializar vector store (pero no lo usamos en MCP por ahora para evitar errores)
vector_store = VectorStore()
try:
    vector_store.build_or_load_faiss_index()
except Exception as e:
    logger.warning(f"VectorStore no inicializado: {e}")

# Inicializar MCP Server CON BASE DE DATOS
mcp_server = MCPDatabaseServer(local_llm)

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
    """Manejar comandos MCP - CON BASE DE DATOS PRIMERO"""
    try:
        if command == "help" or command == "tools":
            tools = mcp_server.list_tools()
            tools_list = "\n".join([f"- **{tool['name']}**: {tool['description']}" for tool in tools])
            return f"""
## 🗄️ **Herramientas MCP (Base de Datos First)**

{tools_list}

**Flujo:** 
1. 🔍 Busca en Base de Datos SQLite
2. 🤖 Solo si no encuentra, usa LLM

**Ejemplos:**
`/mcp {{"tool": "explain_concept", "arguments": {{"concept": "listas"}}}}`
`/mcp {{"tool": "search_knowledge", "arguments": {{"query": "decoradores"}}}}`
"""
        
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
            
            # Ejecutar herramienta CON BASE DE DATOS PRIMERO
            response = await asyncio.wait_for(
                mcp_server.call_tool(tool_name, arguments),
                timeout=45.0
            )
            return response
            
        except json.JSONDecodeError as e:
            return f"❌ Error en formato JSON. Usa: /mcp {{\"tool\": \"nombre\", \"arguments\": {{\"param\": \"valor\"}}}}"
        
    except Exception as e:
        logger.error(f"Error en comando MCP: {e}")
        return f"❌ Error: {str(e)}"

async def agent(prompt):
    """Agente principal con soporte MCP"""
    if not prompt or not prompt.strip():
        return "❌ Por favor, ingresa una pregunta válida."

    user_query = prompt.strip()
    logger.info(f"🔍 Procesando consulta: {user_query}")

    # 1️⃣ Detectar si es un comando MCP (RÁPIDO con base de datos)
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
        Session = sessionmaker(bind=engine)
        with Session() as session:
            db_response = session.query(PythonDB).filter(
                PythonDB.prompt.ilike(f"%{user_query}%")
            ).first()
            
            if db_response:
                logger.info("✅ Respuesta encontrada en base de datos exacta")
                return f"📚 **Respuesta encontrada en base de datos:**\n{db_response.response}"
    except Exception as e:
        logger.error(f"⚠️ Error en consulta SQL: {e}")

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
            
            # También guardar en PythonDB para MCP
            with Session() as session:
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