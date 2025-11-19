from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel import Session

from musica_api.models import Usuario
from musica_api.db import get_session

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[Usuario], summary="Listar usuarios")
def listar_usuarios(session: Session = Depends(get_session)):
    usuarios = session.exec(select(Usuario)).all()
    return usuarios


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    # Verificar correo único
    existing = session.exec(select(Usuario).where(Usuario.correo == usuario.correo)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Correo ya registrado")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.get("/{usuario_id}", response_model=Usuario, summary="Obtener usuario por ID")
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=Usuario, summary="Actualizar usuario")
def actualizar_usuario(usuario_id: int, usuario: Usuario, session: Session = Depends(get_session)):
    db = session.get(Usuario, usuario_id)
    if not db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.nombre = usuario.nombre
    db.correo = usuario.correo
    session.add(db)
    session.commit()
    session.refresh(db)
    return db


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    db = session.get(Usuario, usuario_id)
    if not db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(db)
    session.commit()
    return None
