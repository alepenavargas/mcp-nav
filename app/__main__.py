"""
Punto de entrada para ejecutar el servidor MCP SSE para modelcontextprotocol.io.
"""

import uvicorn
from app import create_app, CONFIG, logger

def main():
    """Función principal para iniciar el servidor MCP desde la línea de comandos."""
    app = create_app()
    
    logger.info(f"Iniciando servidor MCP-NAV en puerto {CONFIG['PORT']}")
    logger.info(f"URL del servidor: http://localhost:{CONFIG['PORT']}/sse")
    
    # Ejecutar con uvicorn
    uvicorn.run(app, host="0.0.0.0", port=CONFIG["PORT"], log_level="info")

# Iniciar el servidor MCP si se ejecuta directamente
if __name__ == "__main__":
    main() 