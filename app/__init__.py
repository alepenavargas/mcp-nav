"""
Módulo principal para la configuración del servidor MCP SSE para modelcontextprotocol.io.
Define las tools y configuraciones necesarias para la navegación web.
"""

import os
import logging
import sys
import urllib.parse
from typing import List

import requests
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup

# --- Configuración de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-nav-sse")

# --- Configuración centralizada ---
CONFIG = {
    "PORT": int(os.environ.get("MCP_NAV_PORT", 9090)),
    "BASE_URL": "https://modelcontextprotocol.io",
    "MAX_LINKS": 20,
}

# --- Definición del servidor MCP ---
mcp = FastMCP(
    name="MCP-NAV",
    description="Navegador para modelcontextprotocol.io"
)

class WebsiteNavigator:
    """Clase para gestionar la navegación en el sitio web."""

    def __init__(self) -> None:
        """Inicializar el navegador con una sesión y estado."""
        self.session = requests.Session()
        self.current_url = CONFIG["BASE_URL"]
        self.history = [CONFIG["BASE_URL"]]
    
    def get_page_content(self, url: str) -> dict:
        """
        Obtener y analizar el contenido de una página.
        
        Args:
            url: La URL o ruta a navegar. Puede ser una URL completa o relativa.
            
        Returns:
            Un diccionario con el contenido y metadatos de la página.
        """
        full_url = url if url.startswith("http") else urllib.parse.urljoin(CONFIG["BASE_URL"], url)
        
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
                if href.startswith("/") or href.startswith(CONFIG["BASE_URL"]):
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
                "links": links[:CONFIG["MAX_LINKS"]],  # Limitar a un número máximo de enlaces
                "html": str(content) if content else ""
            }
        except Exception as e:
            logger.error(f"Error al obtener {full_url}: {e}")
            return {"error": str(e), "url": full_url}

# Instanciar el navegador
navigator = WebsiteNavigator()

# --- Endpoint de healthcheck ---
async def ping_response(request):
    """Endpoint simple para verificar que el servidor está funcionando."""
    return PlainTextResponse("pong")

# --- Definición de herramientas (tools) ---
@mcp.tool()
def navigate(url: str) -> dict:
    """
    Navegar a una URL específica en modelcontextprotocol.io.
    
    Args:
        url: La URL o ruta a navegar. Puede ser una URL completa o relativa.
        
    Returns:
        El contenido y metadatos de la página solicitada.
    """
    return navigator.get_page_content(url)

@mcp.tool()
def current_page() -> dict:
    """
    Obtener el contenido de la página actual.
    
    Returns:
        El contenido y metadatos de la página actual.
    """
    return navigator.get_page_content(navigator.current_url)

@mcp.tool()
def search(query: str) -> List[dict]:
    """
    Buscar contenido en modelcontextprotocol.io.
    
    Args:
        query: La cadena de consulta para buscar.
        
    Returns:
        Lista de resultados de búsqueda que coinciden con la consulta.
    """
    home_content = navigator.get_page_content(CONFIG["BASE_URL"])
    
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
    """
    Obtener el historial de navegación.
    
    Returns:
        Lista de URLs visitadas previamente.
    """
    return navigator.history

@mcp.tool()
def extract_links() -> List[dict]:
    """
    Extraer todos los enlaces de la página actual.
    
    Returns:
        Lista de enlaces y su texto descriptivo.
    """
    page_content = navigator.get_page_content(navigator.current_url)
    return page_content.get("links", [])

@mcp.resource("resource://current_url")
def get_current_url() -> str:
    """
    Obtener la URL actual.
    
    Returns:
        La URL actual que se está visualizando.
    """
    return navigator.current_url

def create_app():
    """
    Crea y configura la aplicación SSE.
    
    Returns:
        La aplicación SSE configurada lista para ser ejecutada.
    """
    # Configurar el puerto mediante una variable de entorno
    os.environ["MCP_HTTP_PORT"] = str(CONFIG["PORT"])
    
    # Convertir a aplicación SSE
    sse = mcp.sse_app()
    
    # Añadir ruta para healthcheck
    sse.routes.append(
        Route("/ping", endpoint=ping_response, methods=["GET"])
    )
    
    return sse 