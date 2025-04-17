"""Implementación del repositorio base para MongoDB."""

from typing import Generic, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.base import BaseDBModel
from app.repositories.base import BaseRepository, T

class MongoRepository(BaseRepository[T], Generic[T]):
    """Implementación del repositorio base usando MongoDB."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """
        Inicializar el repositorio.

        Args:
            collection: Colección de MongoDB a utilizar
        """
        self.collection = collection

    async def get(self, id: str) -> Optional[T]:
        """
        Obtener una entidad por su ID.

        Args:
            id: Identificador único de la entidad

        Returns:
            La entidad si existe, None en caso contrario
        """
        doc = await self.collection.find_one({"_id": id})
        if doc:
            return self._to_model(doc)
        return None

    async def create(self, entity: T) -> T:
        """
        Crear una nueva entidad.

        Args:
            entity: Entidad a crear

        Returns:
            La entidad creada
        """
        doc = self._to_dict(entity)
        await self.collection.insert_one(doc)
        return entity

    async def update(self, entity: T) -> Optional[T]:
        """
        Actualizar una entidad existente.

        Args:
            entity: Entidad con los nuevos datos

        Returns:
            La entidad actualizada si existe, None en caso contrario
        """
        doc = self._to_dict(entity)
        result = await self.collection.replace_one({"_id": entity.id}, doc)
        if result.modified_count:
            return entity
        return None

    async def delete(self, id: str) -> bool:
        """
        Eliminar una entidad por su ID.

        Args:
            id: Identificador único de la entidad

        Returns:
            True si se eliminó correctamente, False si no existía
        """
        result = await self.collection.delete_one({"_id": id})
        return bool(result.deleted_count)

    def _to_dict(self, entity: T) -> dict:
        """
        Convertir una entidad a diccionario para MongoDB.

        Args:
            entity: Entidad a convertir

        Returns:
            Diccionario con los datos de la entidad
        """
        doc = entity.dict()
        if entity.id:
            doc["_id"] = entity.id
            del doc["id"]
        return doc

    def _to_model(self, doc: dict) -> T:
        """
        Convertir un documento de MongoDB a entidad.

        Args:
            doc: Documento de MongoDB

        Returns:
            Entidad convertida
        """
        if "_id" in doc:
            doc["id"] = doc.pop("_id")
        return BaseDBModel.parse_obj(doc)  # type: ignore 