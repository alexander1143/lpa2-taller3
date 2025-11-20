"""Seed script: crea 5 usuarios y 10 canciones en la base de datos.

Ejecutar:
  ./venv/bin/python3 scripts/seed_db.py

El script llama a `init_db()` para asegurar que las tablas existen y luego inserta
los registros si la tabla de usuarios está vacía (evita duplicados al re-ejecutar).
"""
from __future__ import annotations
import sys
import os

# Asegurar que el directorio raíz del proyecto está en sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from init_db import init_db
from musica_api.db import get_engine
from musica_api.models import Usuario, Cancion
from sqlmodel import Session, select


def seed():
    print("Inicializando la base de datos (creando tablas si es necesario)...")
    init_db()

    engine = get_engine()

    usuarios_data = [
        {"nombre": "Ana Perez", "correo": "ana.perez@example.com"},
        {"nombre": "Carlos Gómez", "correo": "carlos.gomez@example.com"},
        {"nombre": "María López", "correo": "maria.lopez@example.com"},
        {"nombre": "Jorge Ramírez", "correo": "jorge.ramirez@example.com"},
        {"nombre": "Lucía Torres", "correo": "lucia.torres@example.com"},
    ]

    canciones_data = [
        {"titulo": "Sol de Medianoche", "artista": "Banda A", "album": "Noches", "duracion": 210, "anio": 2018, "genero": "Rock"},
        {"titulo": "Lluvia en Abril", "artista": "Cantante B", "album": "Estaciones", "duracion": 185, "anio": 2020, "genero": "Pop"},
        {"titulo": "Camino al Mar", "artista": "Duo C", "album": "Viajes", "duracion": 240, "anio": 2015, "genero": "Folk"},
        {"titulo": "Corazón de Piedra", "artista": "Solista D", "album": "Sentires", "duracion": 200, "anio": 2019, "genero": "Balada"},
        {"titulo": "Ritmo Libre", "artista": "Banda E", "album": "Fiesta", "duracion": 195, "anio": 2021, "genero": "Dance"},
        {"titulo": "Horizonte Azul", "artista": "Trío F", "album": "Amaneceres", "duracion": 230, "anio": 2017, "genero": "Instrumental"},
        {"titulo": "Viento del Norte", "artista": "Cantante G", "album": "Territorio", "duracion": 205, "anio": 2016, "genero": "Country"},
        {"titulo": "Noche sin Fin", "artista": "Banda H", "album": "Oscuridad", "duracion": 220, "anio": 2014, "genero": "Rock"},
        {"titulo": "Susurros", "artista": "Solista I", "album": "Intimo", "duracion": 175, "anio": 2022, "genero": "Indie"},
        {"titulo": "Pies en la Tierra", "artista": "Grupo J", "album": "Raíces", "duracion": 210, "anio": 2013, "genero": "Funk"},
    ]

    with Session(engine) as session:
        # Evitar resembrar si ya hay usuarios
        existing_user = session.exec(select(Usuario)).first()
        if existing_user:
            print("La base de datos ya contiene usuarios. No se realizará seed para evitar duplicados.")
            total_u = session.exec(select(Usuario)).all()
            total_c = session.exec(select(Cancion)).all()
            print(f"Usuarios en DB: {len(total_u)}; Canciones en DB: {len(total_c)}")
            return

        print("Insertando usuarios de ejemplo...")
        for u in usuarios_data:
            session.add(Usuario(**u))

        print("Insertando canciones de ejemplo...")
        for s in canciones_data:
            session.add(Cancion(**s))

        session.commit()

        total_u = session.exec(select(Usuario)).all()
        total_c = session.exec(select(Cancion)).all()
        print(f"Seed completado. Usuarios en DB: {len(total_u)}; Canciones en DB: {len(total_c)}")


if __name__ == "__main__":
    seed()
