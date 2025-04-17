"""Base para los repositorios de la aplicación."""

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from app.models.base import BaseDBModel

T = TypeVar('T', bound=BaseDBModel)

class BaseRepository(Generic[T], ABC):
    """Repositorio base para operaciones CRUD."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """
        Obtener una entidad por su ID.

        Args:
            id: Identificador único de la entidad

        Returns:
            La entidad si existe, None en caso contrario
        """
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Crear una nueva entidad.

        Args:
            entity: Entidad a crear

        Returns:
            La entidad creada
        """
        pass

    @abstractmethod
    async def update(self, entity: T) -> Optional[T]:
        """
        Actualizar una entidad existente.

        Args:
            entity: Entidad con los nuevos datos

        Returns:
            La entidad actualizada si existe, None en caso contrario
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """
        Eliminar una entidad por su ID.

        Args:
            id: Identificador único de la entidad

        Returns:
            True si se eliminó correctamente, False si no existía
        """
        pass 