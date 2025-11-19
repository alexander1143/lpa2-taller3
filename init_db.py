"""
Script para inicializar la base de datos.
Crea todas las tablas necesarias para la API de Música.
"""

from sqlmodel import SQLModel, create_engine
from musica_api.config import Settings


def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    settings = Settings()
    engine = create_engine(settings.database_url)
    
    # Importar los modelos para que queden registrados en SQLModel.metadata
    # (esto asegura que SQLModel.metadata contenga las tablas definidas)
    try:
        import musica_api.models  # noqa: F401
    except Exception as e:
        print("Advertencia: no se pudieron importar los modelos:", e)

    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)
    
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()