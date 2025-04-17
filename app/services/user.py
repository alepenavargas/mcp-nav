"""Servicio para la gestión de usuarios."""

from typing import Optional
from ..models.user import User
from ..repositories.user import UserRepository

class UserService:
    """Servicio para gestionar la lógica de negocio relacionada con usuarios."""

    def __init__(self, repository: UserRepository):
        """Inicializa el servicio con su repositorio.
        
        Args:
            repository: Repositorio de usuarios
        """
        self.repository = repository

    async def create_user(self, user_data: dict) -> User:
        """Crea un nuevo usuario.
        
        Args:
            user_data: Datos del usuario a crear
            
        Returns:
            User: Usuario creado
            
        Raises:
            ValueError: Si el email ya existe
        """
        if await self.repository.find_by_email(user_data["email"]):
            raise ValueError("Email already exists")
            
        user = User(**user_data)
        return await self.repository.create(user)

    async def get_user(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            User: Usuario encontrado o None si no existe
        """
        return await self.repository.find_by_id(user_id)

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        """Actualiza los datos de un usuario.
        
        Args:
            user_id: ID del usuario
            user_data: Nuevos datos del usuario
            
        Returns:
            User: Usuario actualizado o None si no existe
        """
        user = await self.repository.find_by_id(user_id)
        if not user:
            return None
            
        for key, value in user_data.items():
            setattr(user, key, value)
            
        return await self.repository.update(user)

    async def delete_user(self, user_id: str) -> bool:
        """Elimina un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se eliminó correctamente
        """
        return await self.repository.delete(user_id)

    async def update_profile_picture(self, user_id: str, picture_url: str) -> Optional[User]:
        """Actualiza la foto de perfil de un usuario.
        
        Args:
            user_id: ID del usuario
            picture_url: URL de la nueva foto
            
        Returns:
            User: Usuario actualizado o None si no existe
        """
        return await self.repository.update_profile_picture(user_id, picture_url) 