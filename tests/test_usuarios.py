import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

# Asegurar que el directorio raíz del proyecto está en sys.path durante pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(name="engine")
def engine_fixture():
    """Engine SQLite en memoria compartida para pruebas."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Importar modelos para registrarlos en metadata
    import musica_api.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Crear una sesión por test usando el engine en memoria."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    """Cliente de FastAPI con override de la dependencia `get_session`."""
    from main import app
    from musica_api.db import get_session

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_session, None)


def test_listar_usuarios_vacio(client: TestClient):
    r = client.get("/api/usuarios/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert r.json() == []


def test_crear_usuario(client: TestClient):
    payload = {"nombre": "Usuario Test", "correo": "test@example.com"}
    r = client.post("/api/usuarios/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["nombre"] == payload["nombre"]
    assert data["correo"] == payload["correo"]
    assert "id" in data


def test_crear_usuario_correo_duplicado(client: TestClient):
    payload = {"nombre": "Usuario A", "correo": "dup@example.com"}
    r1 = client.post("/api/usuarios/", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/usuarios/", json=payload)
    assert r2.status_code == 409


def test_obtener_actualizar_eliminar_usuario(client: TestClient):
    payload = {"nombre": "Usuario CRUD", "correo": "crud@example.com"}
    r = client.post("/api/usuarios/", json=payload)
    assert r.status_code == 201
    user = r.json()
    uid = user["id"]

    # Obtener
    r_get = client.get(f"/api/usuarios/{uid}")
    assert r_get.status_code == 200
    assert r_get.json()["correo"] == payload["correo"]

    # Actualizar
    update = {"nombre": "Usuario Mod", "correo": "mod@example.com"}
    r_put = client.put(f"/api/usuarios/{uid}", json=update)
    assert r_put.status_code == 200
    assert r_put.json()["nombre"] == update["nombre"]
    assert r_put.json()["correo"] == update["correo"]

    # Eliminar
    r_del = client.delete(f"/api/usuarios/{uid}")
    assert r_del.status_code == 204

    # Verificar eliminado
    r_get2 = client.get(f"/api/usuarios/{uid}")
    assert r_get2.status_code == 404
