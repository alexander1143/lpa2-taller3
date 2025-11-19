import sys
import os

# Añadir el directorio raíz del proyecto al PYTHONPATH para poder importar `main`
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def check():
    r_root = client.get("/")
    print("GET / ->", r_root.status_code)
    try:
        print(r_root.json())
    except Exception:
        print("No JSON body for /")

    r = client.get("/api/usuarios/")
    print("GET /api/usuarios/ ->", r.status_code)
    try:
        print(r.json())
    except Exception as e:
        print("No JSON or error reading response:", e)


if __name__ == "__main__":
    check()
