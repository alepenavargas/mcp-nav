"""Endpoints para la gestión de usuarios."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from ..models.user import User, UserCreate, UserUpdate
from ..services.user import UserService
from ..dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
) -> User:
    """Crea un nuevo usuario."""
    try:
        return await service.create_user(user_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=Optional[User])
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Obtiene un usuario por su ID."""
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=Optional[User])
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Actualiza los datos de un usuario."""
    user = await service.update_user(user_id, user_data.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> dict:
    """Elimina un usuario."""
    if await service.delete_user(user_id):
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}/profile-picture", response_model=Optional[User])
async def update_profile_picture(
    user_id: str,
    picture_url: str,
    service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Actualiza la foto de perfil de un usuario."""
    user = await service.update_profile_picture(user_id, picture_url)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 