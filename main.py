from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from musica_api.config import Settings
from init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Inicio y cierre de la aplicación. Crea las tablas si es necesario.
    """
    # Startup: inicializar la base de datos (crea tablas si faltan)
    init_db()
    yield
    # Shutdown: acciones de cierre (si aplica)
    print("cerrando aplicación...")


# Cargar settings con pydantic-settings
settings = Settings()

# Descripción de tags para que aparezcan en la documentación Swagger UI
openapi_tags = [
    {"name": "Root", "description": "Endpoints de información general de la API."},
    {"name": "Health", "description": "Endpoints de verificación de estado de la API."},
    {"name": "Usuarios", "description": "Operaciones relacionadas con usuarios (crear, listar, actualizar)."},
    {"name": "Canciones", "description": "Operaciones relacionadas con canciones (crear, listar, actualizar)."},
    {"name": "Favoritos", "description": "Operaciones para marcar/desmarcar canciones favoritas."},
]


# Crear la instancia de FastAPI con metadatos útiles para Swagger/OpenAPI
app = FastAPI(
    title=settings.app_name,
    description=(
        "API RESTful para gestionar usuarios, canciones y favoritos. "
        "La documentación interactiva (Swagger UI) está disponible en /docs y ReDoc en /redoc."
    ),
    version=settings.app_version,
    lifespan=lifespan,
    openapi_tags=openapi_tags,
    contact={"name": "Equipo de Desarrollo", "email": "dev@example.com"},
    license_info={"name": "MIT"},
)


# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
from musica_api.routers.usuarios import router as usuarios_router
app.include_router(usuarios_router)
from musica_api.routers.canciones import router as canciones_router
from musica_api.routers.favoritos import router as favoritos_router

app.include_router(canciones_router)
app.include_router(favoritos_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    Retorna información básica y enlaces a la documentación interactiva.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check básico. No realiza chequeos profundos aún.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.host, port=8000, reload=True)


