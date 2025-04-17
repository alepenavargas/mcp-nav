"""Punto de entrada para ejecutar el servidor MCP SSE."""

import uvicorn
from app import create_app, CONFIG, logger

def main():
    """Iniciar el servidor MCP."""
    app = create_app()
    
    logger.info(f"Iniciando servidor MCP-NAV en puerto {CONFIG['PORT']}")
    logger.info(f"URL del servidor: http://localhost:{CONFIG['PORT']}/sse")
    logger.info(f"Caché TTL: {CONFIG['CACHE_TTL']} segundos")
    logger.info(f"Mantener HTML: {'Sí' if CONFIG['KEEP_HTML'] else 'No'}")
    
    uvicorn.run(app, host="0.0.0.0", port=CONFIG["PORT"], log_level="info")

if __name__ == "__main__":
    main() 