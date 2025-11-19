from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import Mapped, relationship


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str = Field(index=True, unique=True)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)

    favoritos: Mapped[List["Favorito"]] = relationship(
        "Favorito", back_populates="usuario", cascade="all, delete-orphan"
    )


class Cancion(SQLModel, table=True):
    __tablename__ = "cancion"

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    artista: Optional[str] = None
    album: Optional[str] = None
    duracion: Optional[int] = None  # en segundos
    anio: Optional[int] = None
    genero: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    favoritos: Mapped[List["Favorito"]] = relationship(
        "Favorito", back_populates="cancion", cascade="all, delete-orphan"
    )


class Favorito(SQLModel, table=True):
    __tablename__ = "favorito"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    cancion_id: Optional[int] = Field(default=None, foreign_key="cancion.id")
    fecha_marcado: datetime = Field(default_factory=datetime.utcnow)

    usuario: Mapped[Optional["Usuario"]] = relationship("Usuario", back_populates="favoritos")
    cancion: Mapped[Optional["Cancion"]] = relationship("Cancion", back_populates="favoritos")
