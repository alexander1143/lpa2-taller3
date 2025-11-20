import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

# Asegurar import de paquete
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    import musica_api.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    from main import app
    from musica_api.db import get_session

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_session, None)


def test_crud_cancion(client: TestClient):
    payload = {
        "titulo": "Test Song",
        "artista": "Artist",
        "album": "Album",
        "duracion": 180,
        "anio": 2020,
        "genero": "Pop",
    }

    # crear
    r = client.post("/api/canciones/", json=payload)
    assert r.status_code == 201
    data = r.json()
    cid = data["id"]

    # listar
    r2 = client.get("/api/canciones/")
    assert r2.status_code == 200
    assert any(c["id"] == cid for c in r2.json())

    # obtener
    r3 = client.get(f"/api/canciones/{cid}")
    assert r3.status_code == 200
    assert r3.json()["titulo"] == payload["titulo"]

    # actualizar
    update = {**payload, "titulo": "Nuevo Titulo"}
    r4 = client.put(f"/api/canciones/{cid}", json=update)
    assert r4.status_code == 200
    assert r4.json()["titulo"] == "Nuevo Titulo"

    # buscar
    r5 = client.get("/api/canciones/buscar", params={"titulo": "Nuevo"})
    assert r5.status_code == 200
    assert any("Nuevo" in c["titulo"] for c in r5.json())

    # eliminar
    r6 = client.delete(f"/api/canciones/{cid}")
    assert r6.status_code == 204

    r7 = client.get(f"/api/canciones/{cid}")
    assert r7.status_code == 404
