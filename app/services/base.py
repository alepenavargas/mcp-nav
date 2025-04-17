"""Base para los servicios de la aplicación."""

from typing import Generic, List, Optional, TypeVar
from app.models.base import BaseDBModel
from app.repositories.base import BaseRepository

T = TypeVar('T', bound=BaseDBModel)

class BaseService(Generic[T]):
    """Servicio base para operaciones CRUD."""

    def __init__(self, repository: BaseRepository[T]):
        """Inicializar el servicio.
        
        Args:
            repository: Repositorio para acceder a los datos
        """
        self._repository = repository

    async def get(self, id: str) -> Optional[T]:
        """Obtener una entidad por su ID.
        
        Args:
            id: Identificador único de la entidad
            
        Returns:
            La entidad si existe, None en caso contrario
        """
        return await self._repository.get(id)

    async def get_all(self) -> List[T]:
        """Obtener todas las entidades.
        
        Returns:
            Lista de entidades
        """
        return await self._repository.get_all()

    async def create(self, entity: T) -> T:
        """Crear una nueva entidad.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            La entidad creada
        """
        return await self._repository.create(entity)

    async def update(self, id: str, entity: T) -> Optional[T]:
        """Actualizar una entidad existente.
        
        Args:
            id: Identificador único de la entidad
            entity: Datos actualizados de la entidad
            
        Returns:
            La entidad actualizada si existe, None en caso contrario
        """
        entity.update_timestamp()
        return await self._repository.update(id, entity)

    async def delete(self, id: str) -> bool:
        """Eliminar una entidad.
        
        Args:
            id: Identificador único de la entidad
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        return await self._repository.delete(id) 