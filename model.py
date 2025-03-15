from sqlalchemy import Integer, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base, Session, mapped_column
import datetime

# Definir la base de datos
engine = create_engine("sqlite:///my_database.sqlite", echo=True)

# Definir la base declarativa
Base = declarative_base()

# Crear la tabla ApiKey
class ApiKey(Base):
    __tablename__ = 'api_key'

    id = mapped_column(Integer, primary_key=True)
    key = mapped_column(String(255), nullable=False)
    date = mapped_column(DateTime, default=datetime.datetime.now)

# Crear la tabla History
class History(Base):
    __tablename__ = 'history'

    id = mapped_column(Integer, primary_key=True)
    prompt = mapped_column(String(255), nullable=False)
    response = mapped_column(String(255), nullable=False)
    date = mapped_column(DateTime, default=datetime.datetime.now)


# Crear las tablas en la base de datos
Base.metadata.create_all(engine)  # <-- Esto debe ejecutarse aquí, después de definir las clases


# Crear una clase que maneja la inserción de datos en la tabla History
class HistoryEntry:
    def __init__(self, prompt, response):
        if prompt and response:
            self.prompt = prompt
            self.response = response
            self.save()

    def save(self):
        session = Session(engine)  # Crear sesión SQLAlchemy
        history_entry = History(prompt=self.prompt, response=self.response)
        session.add(history_entry)
        session.commit()
        session.close()
    def selectHistorie(self):
        session = Session(engine)
        query = session.query(History)
        historys = query.all()

        for history in historys:
            print(f"Prompt: {history.prompt} - Response: {history.response}")
        session.close()
    # create a fuction that retieve all the history in a list of strings
    def selectAllHistorie(self):
        session = Session(engine)
        query = session.query(History)
        historys = query.all()
        return historys



# Crear una clase que maneja la inserción de datos en la tabla ApiKey
class ApiKeyEntry:
    def __init__(self, key):
        self.key = key
        if key:
            self.save()

    def save(self):
        session = Session(engine)  # Crear sesión SQLAlchemy
        api_key_entry = ApiKey(key=self.key)
        session.add(api_key_entry)
        session.commit()
        session.close()
    def selectApiKeys(self):
        session = Session(engine)
        query = session.query(ApiKey)
        try:
            api_key = query.all()[0]  # Obtener todas las filas de la tabla
            print(f"API Key: {api_key.key}")
            session.close()
            return api_key.key
        except IndexError:
            print("No se encontraron claves de API en la base de datos.")
            session.close()
            return None

# is api key in the database do not create
apiKeys = ApiKeyEntry(None).selectApiKeys()
if apiKeys is None:
    # Insertar una clave de API en la tabla ApiKey
    apiKey = ApiKeyEntry(key="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")
else:
    apiKey = ApiKeyEntry(None)
