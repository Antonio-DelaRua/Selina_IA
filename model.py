from sqlalchemy import Integer, DateTime, String, create_engine, Column
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Definir la base de datos
engine = create_engine("sqlite:///my_database.sqlite", echo=False)

# Definir la base declarativa
Base = declarative_base()


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)

# Crear la tabla PythonDB
class PythonDB(Base):
    __tablename__ = 'python_db'

    id = Column(Integer, primary_key=True)
    prompt = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now)

    def save(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error al guardar el prompt predefinido: {e}")
        finally:
            session.close()

    @staticmethod
    def get_by_prompt(prompt):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            return session.query(PythonDB).filter(PythonDB.prompt == prompt).first()
        except Exception as e:
            session.rollback()
            print(f"Error al consultar el prompt predefinido: {e}")
        finally:
            session.close()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una clase que maneja la inserción de datos en la tabla History
class HistoryEntry:
    def __init__(self, prompt, response):
        if prompt and response:
            self.prompt = prompt
            self.response = response
           

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

