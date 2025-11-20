import sys
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# create song
payload = {
    "titulo": "Test Song",
    "artista": "Artist",
    "album": "Album",
    "duracion": 180,
    "anio": 2020,
    "genero": "Pop",
}

r = client.post('/api/canciones/', json=payload)
print('POST /api/canciones/ ->', r.status_code)
print(r.json())

cid = r.json().get('id')

r4 = client.put(f"/api/canciones/{cid}", json={**payload, 'titulo':'Nuevo Titulo'})
print('PUT ->', r4.status_code, r4.json())

r5 = client.get('/api/canciones/buscar', params={'titulo':'Nuevo'})
print('GET /api/canciones/buscar ->', r5.status_code)
try:
    print(r5.json())
except Exception as e:
    print('no json', e)
