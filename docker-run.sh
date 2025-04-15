#!/bin/sh

# Función de ayuda
show_help() {
  echo "Uso: ./docker-run.sh [opciones]"
  echo ""
  echo "Opciones:"
  echo "  --build      Solo construir la imagen Docker"
  echo "  --compose    Usar Docker Compose (predeterminado)"
  echo "  --docker     Usar Docker directamente en lugar de Docker Compose"
  echo "  --help       Mostrar esta ayuda"
  echo ""
  echo "Ejemplo: ./docker-run.sh --docker"
}

# Procesar argumentos
USE_COMPOSE=true

for arg in "$@"; do
  case $arg in
    --build)
      BUILD_ONLY=true
      ;;
    --compose)
      USE_COMPOSE=true
      ;;
    --docker)
      USE_COMPOSE=false
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo "Opción desconocida: $arg"
      show_help
      exit 1
      ;;
  esac
done

# Construir la imagen
if [ "$USE_COMPOSE" = true ]; then
  echo "Construyendo la imagen Docker de MCP-NAV con Docker Compose..."
  docker-compose build
else
  echo "Construyendo la imagen Docker de MCP-NAV..."
  docker build -t mcp-nav .
fi

# Si solo queremos construir, terminamos aquí
if [ "$BUILD_ONLY" = true ]; then
  echo "Imagen construida con éxito."
  exit 0
fi

# Verificar si el contenedor ya está en ejecución
if docker ps | grep -q mcp-nav-server; then
  echo "El contenedor ya está en ejecución. Deteniéndolo..."
  if [ "$USE_COMPOSE" = true ]; then
    docker-compose down
  else
    docker stop mcp-nav-server
    docker rm mcp-nav-server
  fi
fi

# Ejecutar el contenedor
if [ "$USE_COMPOSE" = true ]; then
  echo "Iniciando el servidor MCP-NAV con Docker Compose en http://localhost:9090/sse"
  docker-compose up -d
  echo "Contenedor iniciado en segundo plano. Para ver los logs, ejecute: docker-compose logs -f"
else
  echo "Iniciando el servidor MCP-NAV en http://localhost:9090/sse"
  docker run -d -p 9090:9090 --name mcp-nav-server mcp-nav
  echo "Contenedor iniciado en segundo plano. Para ver los logs, ejecute: docker logs -f mcp-nav-server"
fi 