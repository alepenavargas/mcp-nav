"""
Módulo principal para la configuración del servidor MCP SSE para modelcontextprotocol.io.
Define las tools y configuraciones necesarias para la navegación web.
"""

import os
import logging
import sys
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
import html2text
import urllib.parse

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from starlette.routing import Route
from starlette.responses import PlainTextResponse

# --- Configuración centralizada ---
CONFIG = {
    "PORT": int(os.environ.get("MCP_NAV_PORT", 9090)),
    "BASE_URL": "https://modelcontextprotocol.io",
    "CACHE_TTL": int(os.environ.get("MCP_NAV_CACHE_TTL", 3600)),
    "KEEP_HTML": os.environ.get("MCP_NAV_KEEP_HTML", "0") == "1",
    "MAX_RETRIES": 3,
    "RETRY_DELAY": 1
}

# --- Configuración de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-nav")

class Cache:
    """Clase para manejar el caché de páginas."""
    
    def __init__(self, ttl: int = CONFIG["CACHE_TTL"]):
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Dict]:
        """Obtener un valor del caché si existe y no ha expirado."""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry["timestamp"] < timedelta(seconds=self.ttl):
                return entry["data"]
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Dict):
        """Guardar un valor en el caché."""
        self.cache[key] = {
            "data": value,
            "timestamp": datetime.now()
        }
    
    def clear(self):
        """Limpiar el caché."""
        self.cache.clear()

class WebsiteNavigator:
    """Clase para gestionar la navegación en el sitio web."""

    def __init__(self) -> None:
        """Inicializar el navegador con una sesión y estado."""
        self.session = requests.Session()
        self.current_url = CONFIG["BASE_URL"]
        self.history = [CONFIG["BASE_URL"]]
        self.cache = Cache()
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
    
    def _make_request(self, url: str, retries: int = CONFIG["MAX_RETRIES"]) -> requests.Response:
        """Hacer una petición HTTP con reintentos."""
        for attempt in range(retries):
            try:
                response = self.session.get(url)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == retries - 1:
                    raise
                logger.warning(f"Error en intento {attempt + 1}/{retries}: {e}")
                time.sleep(CONFIG["RETRY_DELAY"] * (2 ** attempt))
    
    def get_page_content(self, url: str) -> dict:
        """Obtener y analizar el contenido de una página."""
        full_url = url if url.startswith("http") else urllib.parse.urljoin(CONFIG["BASE_URL"], url)
        
        # Intentar obtener del caché primero
        cached_content = self.cache.get(full_url)
        if cached_content:
            logger.info(f"Contenido obtenido del caché para {full_url}")
            return cached_content
        
        try:
            logger.info(f"Obteniendo contenido de {full_url}")
            response = self._make_request(full_url)
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extraer contenido principal
            content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.find("body")
            
            # Convertir HTML a Markdown
            markdown_content = self.html_converter.handle(str(content)) if content else ""
            
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
            
            # Preparar respuesta
            result = {
                "url": full_url,
                "title": soup.title.string if soup.title else "Sin título",
                "content": markdown_content,
                "links": links[:20],  # Limitar a los primeros 20 enlaces
            }
            
            # Opcionalmente incluir HTML original
            if CONFIG["KEEP_HTML"] and content:
                result["html"] = str(content)
            
            # Guardar en caché
            self.cache.set(full_url, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener {full_url}: {e}")
            return {"error": str(e), "url": full_url}

# --- Crear el servidor MCP ---
mcp = FastMCP(
    name="MCP-NAV",
    description="Navegador para modelcontextprotocol.io con caché y conversión markdown"
)

# Instanciar el navegador
navigator = WebsiteNavigator()

# --- Definición de herramientas ---
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
    """
    Buscar contenido en modelcontextprotocol.io.
    Realiza una búsqueda más profunda incluyendo contenido de las páginas.
    """
    home_content = navigator.get_page_content(CONFIG["BASE_URL"])
    results = []
    
    for link in home_content.get("links", []):
        relevance = 0
        if query.lower() in link["text"].lower():
            relevance += 2  # Mayor peso para coincidencias en títulos
            
        page_content = navigator.get_page_content(link["url"])
        content = page_content.get("content", "").lower()
        
        if query.lower() in content:
            relevance += 1  # Peso para coincidencias en contenido
            
            # Encontrar un snippet relevante
            index = content.find(query.lower())
            start = max(0, index - 100)
            end = min(len(content), index + 100)
            snippet = content[start:end].strip()
            
            if relevance > 0:
                results.append({
                    "title": link["text"],
                    "url": link["url"],
                    "relevance": relevance,
                    "snippet": f"...{snippet}..."
                })
    
    results.sort(key=lambda x: x["relevance"], reverse=True)
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

@mcp.tool()
def clear_cache() -> dict:
    """Limpiar el caché del navegador."""
    navigator.cache.clear()
    return {"status": "success", "message": "Caché limpiado correctamente"}

@mcp.resource("resource://current_url")
def get_current_url() -> str:
    """Obtener la URL actual."""
    return navigator.current_url

# --- Endpoint de healthcheck ---
async def ping_response(request):
    """Endpoint simple para verificar que el servidor está funcionando."""
    return PlainTextResponse("pong")

def create_app():
    """Crear y configurar la aplicación SSE."""
    os.environ["MCP_HTTP_PORT"] = str(CONFIG["PORT"])
    app = mcp.sse_app()
    app.routes.append(Route("/ping", endpoint=ping_response, methods=["GET"]))
    return app 