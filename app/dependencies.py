"""Dependencias para inyección."""

from typing import Generator

from .database import SessionLocal
from .repositories.user import UserRepository
from .services.user import UserService

def get_db() -> Generator:
    """Obtiene una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db=Depends(get_db)) -> UserRepository:
    """Obtiene una instancia del UserRepository."""
    return UserRepository(db)

def get_user_service(repo=Depends(get_user_repository)) -> UserService:
    """Obtiene una instancia del UserService."""
    return UserService(repo) 