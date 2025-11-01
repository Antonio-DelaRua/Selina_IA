from src.core.model import History, engine
from sqlalchemy.orm import sessionmaker

def limpiar_historial():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Eliminar entradas que contengan "ejercicio" en el prompt
        session.query(History).filter(History.prompt.like("%ejercicio%")).delete()
        session.commit()
        print("✅ Historial limpiado correctamente")
    except Exception as e:
        session.rollback()
        print(f"❌ Error al limpiar historial: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    limpiar_historial()