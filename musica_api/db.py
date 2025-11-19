from typing import Generator
from sqlmodel import create_engine, Session
from musica_api.config import Settings

settings = Settings()

# Crear engine reutilizable para la aplicación
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})


def get_engine():
    return engine


def get_session() -> Generator[Session, None, None]:
    """Dependency that yields a SQLModel Session."""
    with Session(engine) as session:
        yield session
