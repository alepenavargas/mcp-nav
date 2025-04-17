"""Modelos Pydantic para usuarios."""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Modelo base para usuarios."""
    email: EmailStr
    name: str
    
class UserCreate(UserBase):
    """Modelo para crear usuarios."""
    password: str

class UserUpdate(BaseModel):
    """Modelo para actualizar usuarios."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    profile_picture: Optional[str] = None

class User(UserBase):
    """Modelo completo de usuario."""
    id: str
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configuración del modelo."""
        from_attributes = True 