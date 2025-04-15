# MCP-NAV

Un servidor MCP (Model Context Protocol) para navegar y acceder al contenido de [modelcontextprotocol.io](https://modelcontextprotocol.io/).

## Características

- Navegar por páginas de modelcontextprotocol.io
- Buscar contenido en el sitio
- Extraer texto y contenido de las páginas
- Seguir enlaces dentro del dominio
- Ver historial de navegación

## Tecnología

Este servidor MCP utiliza:
- **Protocolo de Transporte**: SSE (Server-Sent Events)
- **Puerto**: 9090 (configurable mediante la variable de entorno MCP_NAV_PORT)
- **URL del servidor**: http://localhost:9090/sse

## Estructura del Proyecto

```
mcp-nav/
│
├── app/
│   ├── __init__.py       # Configuración principal y definición de tools
│   └── __main__.py       # Punto de entrada para ejecutar el servidor
│
├── pyproject.toml        # Dependencias y configuración del proyecto
└── README.md             # Documentación del proyecto
```

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/mcp-nav.git
cd mcp-nav

# Instalar con Poetry
poetry install
```

## Uso

```bash
# Iniciar el servidor
poetry run mcp-nav
```

O ejecutar directamente el módulo Python:

```bash
# Iniciar el servidor
poetry run python -m app
```

## Configuración con Cursor

Para usar con Cursor, agrega esta configuración en tu archivo mcp.json:

```json
{
  "mcpServers": {
    "MCP-NAV": {
      "url": "http://localhost:9090/sse"
    }
  }
}
```

## Herramientas disponibles

- `navigate(url)`: Navegar a una URL específica en modelcontextprotocol.io
- `current_page()`: Obtener el contenido de la página actual
- `search(query)`: Buscar contenido en el sitio
- `browse_history()`: Ver historial de navegación
- `extract_links()`: Obtener todos los enlaces de la página actual
- Recurso `current_url`: Acceder a la URL actual

## Verificación del servidor

Puedes verificar que el servidor está funcionando correctamente accediendo a:
```
http://localhost:9090/ping
```

Debería responder con `pong` si el servidor está activo.

## Usando MCP Inspector

Puedes probar el servidor con MCP Inspector:

```bash
npx @modelcontextprotocol/inspector -- poetry run mcp-nav
```

El inspector abrirá una interfaz web en `http://localhost:6274` donde podrás probar todas las herramientas disponibles.

## Variables de Entorno

- `MCP_NAV_PORT`: Puerto en el que se ejecutará el servidor (por defecto: 9090)

## Licencia

MIT 