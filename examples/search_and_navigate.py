#!/usr/bin/env python
"""Ejemplo de cómo utilizar el servidor MCP-NAV desde un script."""

import asyncio
import json
import sys
from pprint import pprint

# Este es un cliente simple para simular cómo un LLM interactuaría con nuestro servidor MCP
# En una aplicación real, usarías la biblioteca MCP client


async def simulate_mcp_client():
    """Simular un cliente MCP para nuestro servidor."""
    # En un caso real, esto sería manejar a través del protocolo MCP
    from app import WebsiteNavigator
    
    navigator = WebsiteNavigator()
    
    # Simular la herramienta navigate
    print("=== Navegando a la página de inicio ===")
    home_page = navigator.get_page_content("https://modelcontextprotocol.io")
    print(f"Título: {home_page['title']}")
    print(f"URL: {home_page['url']}")
    print(f"Primeros 200 caracteres del contenido:")
    print(home_page['content'][:200] + "...")
    
    # Mostrar enlaces disponibles
    print("\n=== Enlaces disponibles en la página actual ===")
    for i, link in enumerate(home_page['links']):
        print(f"{i+1}. {link['text']} -> {link['url']}")
    
    # Simular búsqueda
    query = "Python SDK" if len(sys.argv) < 2 else sys.argv[1]
    print(f"\n=== Buscando '{query}' ===")
    
    results = []
    for link in home_page['links']:
        if query.lower() in link['text'].lower():
            page = navigator.get_page_content(link['url'])
            results.append({
                'title': link['text'],
                'url': link['url'],
                'snippet': page['content'][:100] + "..." if page['content'] else ""
            })
    
    for i, result in enumerate(results):
        print(f"{i+1}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet']}")
    
    # Navegar a un resultado si lo encontramos
    if results:
        print(f"\n=== Navegando al primer resultado: {results[0]['url']} ===")
        page = navigator.get_page_content(results[0]['url'])
        print(f"Título: {page['title']}")
        print(f"Contenido (primeros 300 caracteres):")
        print(page['content'][:300] + "...")
    
    # Mostrar historial
    print("\n=== Historial de navegación ===")
    for i, url in enumerate(navigator.history):
        print(f"{i+1}. {url}")


if __name__ == "__main__":
    asyncio.run(simulate_mcp_client()) 