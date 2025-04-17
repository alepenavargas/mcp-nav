FROM python:3.11-alpine

WORKDIR /app

# Añadir etiquetas recomendadas
LABEL Name="mcp-nav" \
      Version="0.3.0" \
      Description="Servidor MCP para navegar modelcontextprotocol.io con características avanzadas" \
      Maintainer="Your Name <your.email@example.com>"

# Instalar dependencias de compilación necesarias
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copiar archivos del proyecto
COPY pyproject.toml README.md ./
COPY app/ ./app/

# Instalar poetry y dependencias
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

# Exponer el puerto y configurar variables de entorno
ENV MCP_NAV_PORT=9090
ENV MCP_NAV_HOST=0.0.0.0
ENV MCP_NAV_REDIS_HOST=localhost
ENV MCP_NAV_REDIS_PORT=6379
ENV MCP_NAV_ES_HOST=localhost
ENV MCP_NAV_ES_PORT=9200
ENV MCP_NAV_CACHE_TTL=3600
ENV MCP_NAV_JWT_SECRET=your-secret-key

EXPOSE 9090

# Reducir privilegios
RUN addgroup -S mcp && adduser -S mcp -G mcp
USER mcp

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --spider --quiet http://localhost:9090/ping || exit 1

# Comando para ejecutar el servidor
CMD ["python", "-m", "app"] 