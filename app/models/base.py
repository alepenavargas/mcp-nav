"""Modelo base para todas las entidades."""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BaseDBModel(BaseModel):
    """Modelo base con campos comunes para todas las entidades."""

    id: Optional[str] = Field(None, description="Identificador único de la entidad")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    def update_timestamp(self) -> None:
        """Actualizar el timestamp de modificación."""
        self.updated_at = datetime.utcnow()

    class Config:
        """Configuración del modelo."""
        
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        } 