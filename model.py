from sqlalchemy import Integer, DateTime, String, create_engine, Column, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import numpy as np
import json
import logging

logger = logging.getLogger(__name__)

# Definir la base de datos
engine = create_engine("sqlite:///my_database.sqlite", echo=False)
Base = declarative_base()

class BaseModel:
    """Clase base con métodos comunes"""
    
    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            session.add(self)
            session.commit()
            logger.info(f"✅ Registro guardado en {self.__tablename__}")
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error al guardar en {self.__tablename__}: {e}")
            raise
        finally:
            session.close()

    def set_embedding(self, embedding_vector):
        """Set embedding as JSON string"""
        try:
            if isinstance(embedding_vector, np.ndarray):
                self.embedding = json.dumps(embedding_vector.tolist())
            else:
                self.embedding = json.dumps(embedding_vector)
        except Exception as e:
            logger.error(f"❌ Error estableciendo embedding: {e}")

    def get_embedding(self):
        """Get embedding as numpy array"""
        try:
            if self.embedding:
                return np.array(json.loads(self.embedding))
            return None
        except Exception as e:
            logger.error(f"❌ Error obteniendo embedding: {e}")
            return None

class History(Base, BaseModel):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(255), nullable=False)
    response = Column(Text, nullable=False)
    embedding = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.datetime.now)

class PythonDB(Base, BaseModel):
    __tablename__ = 'python_db'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(255), nullable=False)
    response = Column(Text, nullable=False)
    embedding = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.datetime.now)

    @staticmethod
    def get_by_prompt(prompt):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(PythonDB).filter(PythonDB.prompt == prompt).first()
        except Exception as e:
            logger.error(f"❌ Error consultando PythonDB: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_all_with_embeddings():
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(PythonDB).filter(PythonDB.embedding.isnot(None)).all()
        except Exception as e:
            logger.error(f"❌ Error obteniendo embeddings de PythonDB: {e}")
            return []
        finally:
            session.close()

# Crear las tablas
Base.metadata.create_all(engine)

class HistoryEntry:
    def __init__(self, prompt, response):
        if not prompt or not response:
            raise ValueError("Prompt y response son requeridos")
            
        self.prompt = prompt
        self.response = response
        self.embedding = None

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            history_entry = History(
                prompt=self.prompt, 
                response=self.response, 
                embedding=self.embedding
            )
            session.add(history_entry)
            session.commit()
            logger.info("✅ Entrada de historial guardada")
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error guardando historial: {e}")
            raise
        finally:
            session.close()

    def set_embedding(self, embedding_vector):
        """Set embedding as JSON string"""
        try:
            if isinstance(embedding_vector, np.ndarray):
                self.embedding = json.dumps(embedding_vector.tolist())
            else:
                self.embedding = json.dumps(embedding_vector)
        except Exception as e:
            logger.error(f"❌ Error estableciendo embedding en HistoryEntry: {e}")

    def get_embedding(self):
        """Get embedding as numpy array"""
        try:
            if self.embedding:
                return np.array(json.loads(self.embedding))
            return None
        except Exception as e:
            logger.error(f"❌ Error obteniendo embedding de HistoryEntry: {e}")
            return None

    @staticmethod
    def get_by_prompt(prompt):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(History).filter(History.prompt == prompt).first()
        except Exception as e:
            logger.error(f"❌ Error consultando historial: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_all_with_embeddings():
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(History).filter(History.embedding.isnot(None)).all()
        except Exception as e:
            logger.error(f"❌ Error obteniendo embeddings de historial: {e}")
            return []
        finally:
            session.close()