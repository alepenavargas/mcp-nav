"""Configuración central de la aplicación."""

import os
from typing import Dict, Any

class Settings:
    """Configuración de la aplicación."""
    
    # Servidor
    PORT: int = int(os.environ.get("MCP_NAV_PORT", 9090))
    HOST: str = os.environ.get("MCP_NAV_HOST", "0.0.0.0")
    BASE_URL: str = "https://modelcontextprotocol.io"
    
    # Redis
    REDIS_HOST: str = os.environ.get("MCP_NAV_REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("MCP_NAV_REDIS_PORT", 6379))
    REDIS_DB: int = int(os.environ.get("MCP_NAV_REDIS_DB", 0))
    
    # Elasticsearch
    ES_HOST: str = os.environ.get("MCP_NAV_ES_HOST", "localhost")
    ES_PORT: int = int(os.environ.get("MCP_NAV_ES_PORT", 9200))
    
    # Caché
    CACHE_TTL: int = int(os.environ.get("MCP_NAV_CACHE_TTL", 3600))
    KEEP_HTML: bool = os.environ.get("MCP_NAV_KEEP_HTML", "0") == "1"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.environ.get("MCP_NAV_RATE_LIMIT", 100))
    RATE_LIMIT_WINDOW: int = int(os.environ.get("MCP_NAV_RATE_WINDOW", 60))
    
    # Auth
    JWT_SECRET: str = os.environ.get("MCP_NAV_JWT_SECRET", "your-secret-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = int(os.environ.get("MCP_NAV_JWT_EXPIRES", 30))
    
    # Reintentos
    MAX_RETRIES: int = int(os.environ.get("MCP_NAV_MAX_RETRIES", 3))
    RETRY_DELAY: int = int(os.environ.get("MCP_NAV_RETRY_DELAY", 1))
    
    def get_redis_url(self) -> str:
        """Obtener URL de conexión a Redis."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    def get_es_url(self) -> str:
        """Obtener URL de conexión a Elasticsearch."""
        return f"http://{self.ES_HOST}:{self.ES_PORT}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir configuración a diccionario."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }

settings = Settings() 