# MCP-NAV con Docker

Este documento describe cómo ejecutar el servidor MCP-NAV utilizando Docker.

## Requisitos

- Docker instalado en su sistema
- Docker Compose (opcional, recomendado)
- Permisos para ejecutar comandos Docker

## Opciones para ejecutar el servidor

Hay varias formas de ejecutar el servidor MCP-NAV con Docker:

### 1. Usando el script de ayuda (Recomendado)

El método más sencillo es utilizar el script de ayuda incluido:

```bash
# Hacer el script ejecutable (solo necesario la primera vez)
chmod +x docker-run.sh

# Ejecutar con Docker Compose (predeterminado)
./docker-run.sh

# O ejecutar directamente con Docker
./docker-run.sh --docker

# Solo construir la imagen sin ejecutar
./docker-run.sh --build

# Ver todas las opciones disponibles
./docker-run.sh --help
```

### 2. Usando Docker Compose

Si prefiere usar Docker Compose directamente:

```bash
# Construir la imagen
docker-compose build

# Iniciar el servidor en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener el servidor
docker-compose down
```

### 3. Usando Docker directamente

Si prefiere usar Docker sin Docker Compose:

```bash
# Construir la imagen
docker build -t mcp-nav .

# Iniciar el servidor
docker run -d -p 9090:9090 --name mcp-nav-server mcp-nav

# Ver logs
docker logs -f mcp-nav-server

# Detener y eliminar el contenedor
docker stop mcp-nav-server
docker rm mcp-nav-server
```

## Verificación del servidor

Para verificar que el servidor está funcionando correctamente, acceda a:

```
http://localhost:9090/ping
```

Debería responder con `pong` si el servidor está activo.

## Configuración con Cursor

Para usar con Cursor, agregue esta configuración en su archivo mcp.json:

```json
{
  "mcpServers": {
    "MCP-NAV": {
      "url": "http://localhost:9090/sse"
    }
  }
}
```

## Personalización del puerto

Si desea utilizar un puerto diferente:

1. **Con Docker Compose**: Edite el archivo `docker-compose.yml` y cambie los valores del puerto.

2. **Con Docker directamente**:
   ```bash
   docker run -d -p 8080:8080 -e MCP_NAV_PORT=8080 --name mcp-nav-server mcp-nav
   ```

## Sobre la imagen Docker

La imagen Docker utiliza:
- Base mínima: Python 3.11 con Alpine Linux
- Construcción en dos etapas para reducir el tamaño final
- Usuario no privilegiado para mayor seguridad
- Healthcheck para verificar la disponibilidad del servicio 