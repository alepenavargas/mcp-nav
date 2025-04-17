# MCP-NAV v0.2.0

Un servidor MCP (Model Context Protocol) para navegar y acceder al contenido de [modelcontextprotocol.io](https://modelcontextprotocol.io/).

## Características

- Navegación web con caché inteligente
- Búsqueda semántica con ponderación de relevancia
- Conversión automática HTML a Markdown
- Sistema de reintentos con backoff exponencial
- Gestión de memoria optimizada
- Healthcheck integrado
- Seguridad mejorada con usuario no privilegiado
- Soporte para Docker

## Tecnología

- **Runtime**: Python 3.8+
- **Framework**: FastMCP 1.3.0+
- **Transporte**: SSE (Server-Sent Events)
- **Puerto**: 9090 (configurable)
- **Caché**: En memoria con TTL
- **Contenedorización**: Docker + Docker Compose

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

### Usando Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd mcp-nav

# Construir y ejecutar con Docker Compose
docker-compose up -d
```

### Instalación Local

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd mcp-nav

# Instalar con Poetry
poetry install

# O con pip
pip install -e .
```

## Uso

### Con Docker

```bash
# Iniciar el servidor
docker-compose up -d

# Ver logs
docker logs mcp-nav-server

# Detener el servidor
docker-compose down
```

### Sin Docker

```bash
# Iniciar con Poetry
poetry run python -m app

# O directamente con Python
python -m app
```

## Configuración

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `MCP_NAV_PORT` | Puerto del servidor | 9090 |
| `MCP_NAV_CACHE_TTL` | TTL del caché en segundos | 3600 |
| `MCP_NAV_KEEP_HTML` | Mantener HTML en respuestas | 0 |

### Docker Compose

El archivo `docker-compose.yml` incluye:
- Healthcheck configurado
- Reinicio automático
- Mapeo de puertos
- Variables de entorno predefinidas

## API y Herramientas

### Herramientas MCP

- `navigate(url)`: Navegar a una URL
- `current_page()`: Obtener página actual
- `search(query)`: Búsqueda inteligente
- `browse_history()`: Ver historial
- `extract_links()`: Obtener enlaces
- `clear_cache()`: Limpiar caché
- `current_url` (recurso): URL actual

### Endpoints HTTP

- `GET /sse`: Endpoint SSE principal
- `GET /ping`: Healthcheck

## Características Avanzadas

### Sistema de Caché

- Almacenamiento en memoria con TTL configurable
- Invalidación automática
- Gestión eficiente de memoria
- Estadísticas de hit/miss

### Búsqueda Inteligente

- Ponderación de relevancia (título: 2x, contenido: 1x)
- Snippets contextuales
- Ordenamiento por relevancia
- Búsqueda en contenido completo

### Gestión de Errores

- Reintentos automáticos
- Backoff exponencial
- Logging detallado
- Recuperación de fallos

### Seguridad

- Usuario no privilegiado en Docker
- Sanitización de URLs
- Validación de dominios
- Límites de tamaño configurables

## Monitoreo

### Healthcheck

```bash
# Verificar estado
curl http://localhost:9090/ping
# Respuesta esperada: pong
```

### Logs

```bash
# Con Docker
docker logs mcp-nav-server

# Sin Docker
tail -f mcp-nav.log
```

## Desarrollo

### Requisitos

- Python 3.8+
- Poetry o pip
- Docker y Docker Compose (opcional)

### Setup Desarrollo

```bash
# Instalar dependencias de desarrollo
poetry install --with dev

# Ejecutar tests
poetry run pytest
```

## Licencia

MIT 