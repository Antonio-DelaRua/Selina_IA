"""
Gestión de embeddings y búsqueda semántica
"""
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json
import logging
from pathlib import Path
from config.settings import EMBEDDING_MODEL, EMB_DIM, INDEX_PATH, METADATA_PATH

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.metadata = []

    def load_embeddings_from_db(self):
        """Cargar embeddings guardados en PythonDB + History"""
        from .database import SessionLocal, PythonDB, History

        with SessionLocal() as session:
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
            self.index = faiss.read_index(str(INDEX_PATH))
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

                faiss.write_index(self.index, str(INDEX_PATH))
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
            faiss.write_index(self.index, str(INDEX_PATH))
            with open(METADATA_PATH, 'w') as f:
                json.dump(self.metadata, f, default=str)

            logger.info("✅ Nuevo vector agregado al índice.")
            return True
        except Exception as e:
            logger.error(f"❌ Error agregando al índice: {e}")
            return False

# Inicializar vector store
vector_store = VectorStore()
try:
    vector_store.build_or_load_faiss_index()
except Exception as e:
    logger.warning(f"VectorStore no inicializado: {e}")

def generate_embedding(text):
    """Generar embedding numpy para un texto"""
    return vector_store.embedding_model.encode(text, normalize_embeddings=True).astype(np.float32)

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