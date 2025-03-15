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
        histrys = query.all()

        for histry in histrys:
            print(f"Prompt: {histry.prompt} - Response: {histry.response}")
        session.close()