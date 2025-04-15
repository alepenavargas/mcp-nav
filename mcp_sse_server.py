"""Servidor MCP para navegar modelcontextprotocol.io utilizando el transporte SSE."""

import logging
import urllib.parse
import os
import sys
from typing import List

import uvicorn
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from starlette.routing import Route
from starlette.responses import PlainTextResponse

# Configuración básica
PORT = 9091  # Cambiado de 9090 a 9091 para evitar conflictos
BASE_URL = "https://modelcontextprotocol.io"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-nav-sse")

# Crear el objeto MCP 
mcp = FastMCP(
    name="MCP-NAV",
    description="Navegador para modelcontextprotocol.io"
)

class WebsiteNavigator:
    """Clase para gestionar la navegación en el sitio web."""

    def __init__(self) -> None:
        """Inicializar el navegador con una sesión y estado."""
        self.session = requests.Session()
        self.current_url = BASE_URL
        self.history = [BASE_URL]
    
    def get_page_content(self, url: str) -> dict:
        """Obtener y analizar el contenido de una página."""
        full_url = url if url.startswith("http") else urllib.parse.urljoin(BASE_URL, url)
        
        try:
            logger.info(f"Obteniendo contenido de {full_url}")
            response = self.session.get(full_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extraer contenido principal
            content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.find("body")
            
            # Extraer enlaces de la página
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                # Solo incluir enlaces al mismo dominio
                if href.startswith("/") or href.startswith(BASE_URL):
                    links.append({
                        "text": a.get_text().strip(),
                        "url": href
                    })
            
            # Actualizar URL actual e historial
            self.current_url = full_url
            if full_url not in self.history:
                self.history.append(full_url)
            
            return {
                "url": full_url,
                "title": soup.title.string if soup.title else "Sin título",
                "content": content.get_text("\n", strip=True) if content else "",
                "links": links[:20],  # Limitar a los primeros 20 enlaces
                "html": str(content) if content else ""
            }
        except Exception as e:
            logger.error(f"Error al obtener {full_url}: {e}")
            return {"error": str(e), "url": full_url}

# Instanciar el navegador
navigator = WebsiteNavigator()

# Endpoint para verificar que el servidor está funcionando
async def ping_response(request):
    return PlainTextResponse("pong")

@mcp.tool()
def navigate(url: str) -> dict:
    """Navegar a una URL específica en modelcontextprotocol.io."""
    return navigator.get_page_content(url)

@mcp.tool()
def current_page() -> dict:
    """Obtener el contenido de la página actual."""
    return navigator.get_page_content(navigator.current_url)

@mcp.tool()
def search(query: str) -> List[dict]:
    """Buscar contenido en modelcontextprotocol.io."""
    home_content = navigator.get_page_content(BASE_URL)
    
    results = []
    for link in home_content.get("links", []):
        if query.lower() in link["text"].lower():
            page_content = navigator.get_page_content(link["url"])
            results.append({
                "title": link["text"],
                "url": link["url"],
                "snippet": page_content.get("content", "")[:200] + "..." if page_content.get("content") else ""
            })
    
    return results

@mcp.tool()
def browse_history() -> List[str]:
    """Obtener el historial de navegación."""
    return navigator.history

@mcp.tool()
def extract_links() -> List[dict]:
    """Extraer todos los enlaces de la página actual."""
    page_content = navigator.get_page_content(navigator.current_url)
    return page_content.get("links", [])

@mcp.resource("resource://current_url")
def get_current_url() -> str:
    """Obtener la URL actual."""
    return navigator.current_url

def main():
    """Función principal para iniciar el servidor desde la línea de comandos."""
    # Configurar el puerto mediante una variable de entorno
    os.environ["MCP_HTTP_PORT"] = str(PORT)
    
    # Convertir a aplicación SSE
    app = mcp.sse_app()
    
    # Añadir el endpoint /ping para verificaciones
    app.routes.append(
        Route("/ping", endpoint=ping_response, methods=["GET"])
    )
    
    logger.info(f"Iniciando servidor MCP-NAV en puerto {PORT}")
    logger.info(f"URL del servidor: http://localhost:{PORT}/sse")
    
    # Ejecutar con uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")

# Si se ejecuta directamente
if __name__ == "__main__":
    main() 