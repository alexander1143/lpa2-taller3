from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session

from musica_api.models import Favorito, Usuario, Cancion
from musica_api.db import get_session

router = APIRouter(prefix="/api/favoritos", tags=["Favoritos"]) 


@router.get("/", response_model=List[Favorito], summary="Listar favoritos")
def listar_favoritos(session: Session = Depends(get_session)):
    favs = session.exec(select(Favorito)).all()
    return favs


@router.post("/", response_model=Favorito, status_code=status.HTTP_201_CREATED, summary="Marcar favorito")
def crear_favorito(favorito: Favorito, session: Session = Depends(get_session)):
    # verificar usuario y canción
    if not session.get(Usuario, favorito.usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not session.get(Cancion, favorito.cancion_id):
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    # evitar duplicados
    existing = session.exec(
        select(Favorito).where(
            Favorito.usuario_id == favorito.usuario_id, Favorito.cancion_id == favorito.cancion_id
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Favorito ya existe")
    session.add(favorito)
    session.commit()
    session.refresh(favorito)
    return favorito


@router.get("/{favorito_id}", response_model=Favorito, summary="Obtener favorito por ID")
def obtener_favorito(favorito_id: int, session: Session = Depends(get_session)):
    fav = session.get(Favorito, favorito_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    return fav


@router.delete("/{favorito_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar favorito")
def eliminar_favorito(favorito_id: int, session: Session = Depends(get_session)):
    fav = session.get(Favorito, favorito_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    session.delete(fav)
    session.commit()
    return None


# Endpoints específicos por usuario


@router.get("/usuarios/{usuario_id}", response_model=List[Favorito], summary="Listar favoritos de usuario")
def listar_favoritos_usuario(usuario_id: int, session: Session = Depends(get_session)):
    if not session.get(Usuario, usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    favs = session.exec(select(Favorito).where(Favorito.usuario_id == usuario_id)).all()
    return favs


@router.post("/usuarios/{usuario_id}/favoritos/{cancion_id}", status_code=status.HTTP_201_CREATED, summary="Marcar favorito específico")
def marcar_favorito_especifico(usuario_id: int, cancion_id: int, session: Session = Depends(get_session)):
    if not session.get(Usuario, usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not session.get(Cancion, cancion_id):
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    existing = session.exec(
        select(Favorito).where(Favorito.usuario_id == usuario_id, Favorito.cancion_id == cancion_id)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Favorito ya existe")
    fav = Favorito(usuario_id=usuario_id, cancion_id=cancion_id)
    session.add(fav)
    session.commit()
    session.refresh(fav)
    return fav


@router.delete("/usuarios/{usuario_id}/favoritos/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar favorito específico")
def eliminar_favorito_especifico(usuario_id: int, cancion_id: int, session: Session = Depends(get_session)):
    fav = session.exec(
        select(Favorito).where(Favorito.usuario_id == usuario_id, Favorito.cancion_id == cancion_id)
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    session.delete(fav)
    session.commit()
    return None
