from sqlalchemy import Integer, DateTime, String, create_engine, Column
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Definir la base de datos
engine = create_engine("sqlite:///my_database.sqlite", echo=True)

# Definir la base declarativa
Base = declarative_base()

# Crear la tabla ApiKey
class ApiKey(Base):
    __tablename__ = 'api_key'

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)

# Crear la tabla History
class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una clase que maneja la inserción de datos en la tabla History
class HistoryEntry:
    def __init__(self, prompt, response):
        if prompt and response:
            self.prompt = prompt
            self.response = response
            self.save()

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        history_entry = History(prompt=self.prompt, response=self.response)
        try:
            session.add(history_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al guardar el historial: {e}")
        finally:
            session.close()

    @staticmethod
    def get_by_prompt(prompt):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(History).filter(History.prompt == prompt).first()
        except Exception as e:
            session.rollback()
            print(f"Error al consultar el historial: {e}")
        finally:
            session.close()

# Crear una clase que maneja la inserción de datos en la tabla ApiKey
class ApiKeyEntry:
    def __init__(self, key):
        self.key = key
        if key:
            self.save()

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        api_key_entry = ApiKey(key=self.key)
        try:
            session.add(api_key_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al guardar la clave de API: {e}")
        finally:
            session.close()

    @staticmethod
    def select_api_key():
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            api_key = session.query(ApiKey).first()
            if api_key:
                print(f"API Key: {api_key.key}")
                return api_key.key
            else:
                print("No se encontraron claves de API en la base de datos.")
                return None
        finally:
            session.close()

# Verificar si la clave de API está en la base de datos, si no, crear una
api_key = ApiKeyEntry.select_api_key()
if not api_key:
    ApiKeyEntry(key="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")