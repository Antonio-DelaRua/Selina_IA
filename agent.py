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

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🚀 Modelo de embeddings local
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
EMB_DIM = 384
INDEX_PATH = "vector_index.faiss"
METADATA_PATH = "vector_metadata.json"

# 🚀 LLM local (CodeLlama)
local_llm = OllamaLLM(
    model="codellama:latest",
    temperature=0.3,
    num_predict=900,
    repeat_penalty=1.2,
    num_gpu_layers=20,
)

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        
    def load_embeddings_from_db(self):
        """Cargar embeddings guardados en PythonDB + History"""
        Session = sessionmaker(bind=engine)
        session = Session()
        all_entries = []
        
        try:
            # Cargar de PythonDB
            python_entries = session.query(PythonDB).filter(PythonDB.embedding.isnot(None)).all()
            for e in python_entries:
                try:
                    emb = np.array(json.loads(e.embedding), dtype=np.float32)
                    all_entries.append({
                        'embedding': emb,
                        'response': e.response,
                        'prompt': e.prompt,
                        'source': 'python_db',
                        'id': e.id
                    })
                except Exception as e:
                    logger.warning(f"Error cargando embedding de PythonDB: {e}")
                    continue
            
            # Cargar de History
            history_entries = session.query(History).filter(History.embedding.isnot(None)).all()
            for e in history_entries:
                try:
                    emb = np.array(json.loads(e.embedding), dtype=np.float32)
                    all_entries.append({
                        'embedding': emb,
                        'response': e.response,
                        'prompt': e.prompt,
                        'source': 'history',
                        'id': e.id
                    })
                except Exception as e:
                    logger.warning(f"Error cargando embedding de History: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error en load_embeddings_from_db: {e}")
        finally:
            session.close()
            
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

async def agent(prompt):
    """Agente principal mejorado"""
    if not prompt or not prompt.strip():
        return "❌ Por favor, ingresa una pregunta válida."

    user_query = prompt.strip()
    
    logger.info(f"🔍 Procesando consulta: {user_query}")

    # 1️⃣ Buscar en FAQs (mejorado)
    faq_response = search_in_faqs(user_query)
    if faq_response:
        logger.info("✅ Respuesta encontrada en FAQs")
        return f"🔍 **Respuesta oficial:**\n{faq_response}"

    # 2️⃣ Buscar semánticamente en embeddings locales
    semantic_response = semantic_search(user_query)
    if semantic_response:
        logger.info("✅ Respuesta encontrada por búsqueda semántica")
        return f"📘 **Respuesta encontrada en base de conocimientos:**\n{semantic_response}"

    # 3️⃣ Buscar en base de datos exacta
    try:
        db_response = PythonDB.get_by_prompt(user_query) or HistoryEntry.get_by_prompt(user_query)
        if db_response:
            logger.info("✅ Respuesta encontrada en base de datos exacta")
            return f"📚 **Respuesta encontrada en base de datos:**\n{db_response.response}"
    except Exception as e:
        logger.error(f"⚠️ Error en consulta SQL: {e}")

    # 4️⃣ Si no hay coincidencia, usar CodeLlama
    logger.info("🤖 Generando respuesta con LLM")
    prompt_template = f"""
Eres un asistente de IA especializado en desarrollo de software. Responde de manera útil y precisa.

**Instrucciones:**
- Responde ÚNICAMENTE a preguntas relacionadas con programación, código, o temas técnicos
- Si la pregunta NO es sobre programación/código, responde amablemente que solo puedes ayudar con temas técnicos
- Usa español natural con emojis cuando sea apropiado ✨
- Incluye código Python breve si es relevante usando ```python
- Sé conciso pero informativo

**Pregunta del usuario:** {user_query}

**Respuesta:**
"""
    
    try:
        response = await chat_with_codellama(prompt_template)
        
        # 5️⃣ Guardar en historial y actualizar índice FAISS
        embedding = generate_embedding(user_query)
        history_entry = HistoryEntry(prompt=user_query, response=response)
        history_entry.set_embedding(embedding)
        history_entry.save()

        # Agregar al índice FAISS
        vector_store.add_to_index(embedding, user_query, response, "history")
        
        logger.info("✅ Respuesta generada y guardada exitosamente")
        return f"💡 **Respuesta generada por IA:**\n{response}"
        
    except Exception as e:
        logger.error(f"❌ Error en el agente: {e}")
        return f"❌ Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}"