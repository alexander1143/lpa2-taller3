from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel import Session

from musica_api.models import Cancion
from musica_api.db import get_session

router = APIRouter(prefix="/api/canciones", tags=["Canciones"])


@router.get("/", response_model=List[Cancion], summary="Listar canciones")
def listar_canciones(session: Session = Depends(get_session), limit: int = Query(100, ge=1)):
    canciones = session.exec(select(Cancion).limit(limit)).all()
    return canciones


@router.post("/", response_model=Cancion, status_code=status.HTTP_201_CREATED, summary="Crear canción")
def crear_cancion(cancion: Cancion, session: Session = Depends(get_session)):
    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion


@router.get("/buscar", response_model=List[Cancion], summary="Buscar canciones")
def buscar_canciones(
    titulo: Optional[str] = Query(None),
    artista: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Cancion)
    if titulo:
        query = query.where(Cancion.titulo.ilike(f"%{titulo}%"))
    if artista:
        query = query.where(Cancion.artista.ilike(f"%{artista}%"))
    if genero:
        query = query.where(Cancion.genero.ilike(f"%{genero}%"))
    results = session.exec(query).all()
    return results


@router.get("/{cancion_id}", response_model=Cancion, summary="Obtener canción por ID")
def obtener_cancion(cancion_id: int, session: Session = Depends(get_session)):
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion


@router.put("/{cancion_id}", response_model=Cancion, summary="Actualizar canción")
def actualizar_cancion(cancion_id: int, cancion: Cancion, session: Session = Depends(get_session)):
    db = session.get(Cancion, cancion_id)
    if not db:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db.titulo = cancion.titulo
    db.artista = cancion.artista
    db.album = cancion.album
    db.duracion = cancion.duracion
    db.anio = cancion.anio
    db.genero = cancion.genero
    session.add(db)
    session.commit()
    session.refresh(db)
    return db


@router.delete("/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar canción")
def eliminar_cancion(cancion_id: int, session: Session = Depends(get_session)):
    db = session.get(Cancion, cancion_id)
    if not db:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    session.delete(db)
    session.commit()
    return None


@router.get("/buscar", response_model=List[Cancion], summary="Buscar canciones")
def buscar_canciones(
    titulo: Optional[str] = Query(None),
    artista: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Cancion)
    if titulo:
        query = query.where(Cancion.titulo.ilike(f"%{titulo}%"))
    if artista:
        query = query.where(Cancion.artista.ilike(f"%{artista}%"))
    if genero:
        query = query.where(Cancion.genero.ilike(f"%{genero}%"))
    results = session.exec(query).all()
    return results
