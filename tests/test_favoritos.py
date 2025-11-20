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


def create_user_and_song(client: TestClient):
    u = {"nombre": "Fav User", "correo": "fav@example.com"}
    r1 = client.post("/api/usuarios/", json=u)
    assert r1.status_code == 201
    user = r1.json()

    s = {"titulo": "Fav Song", "artista": "A"}
    r2 = client.post("/api/canciones/", json=s)
    assert r2.status_code == 201
    song = r2.json()

    return user, song


def test_favoritos_flow(client: TestClient):
    user, song = create_user_and_song(client)
    uid = user["id"]
    sid = song["id"]

    # marcar favorito específico
    r = client.post(f"/api/favoritos/usuarios/{uid}/favoritos/{sid}")
    assert r.status_code == 201
    fav = r.json()

    # listar favoritos
    r2 = client.get("/api/favoritos/")
    assert r2.status_code == 200
    assert any(f["id"] == fav["id"] for f in r2.json())

    # listar favoritos de usuario
    r3 = client.get(f"/api/favoritos/usuarios/{uid}")
    assert r3.status_code == 200
    assert any(f["cancion_id"] == sid for f in r3.json())

    # eliminar favorito específico
    r4 = client.delete(f"/api/favoritos/usuarios/{uid}/favoritos/{sid}")
    assert r4.status_code == 204

    # verificar eliminado
    r5 = client.get(f"/api/favoritos/usuarios/{uid}")
    assert r5.status_code == 200
    assert all(f["cancion_id"] != sid for f in r5.json())
