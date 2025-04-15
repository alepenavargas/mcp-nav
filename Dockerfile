FROM python:3.11-alpine

WORKDIR /app

# Añadir etiquetas recomendadas
LABEL Name="mcp-nav" \
      Version="0.1.0" \
      Description="Servidor MCP para navegar modelcontextprotocol.io" \
      Maintainer="Your Name <your.email@example.com>"

# Instalar dependencias de compilación necesarias
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copiar archivos del proyecto
COPY pyproject.toml ./
COPY app/ ./app/
COPY mcp_sse_server.py ./

# Instalar dependencias
RUN pip install --no-cache-dir -e .

# Exponer el puerto y configurar variables de entorno
ENV MCP_NAV_PORT=9090
EXPOSE 9090

# Reducir privilegios
RUN addgroup -S mcp && adduser -S mcp -G mcp
USER mcp

# Comando para ejecutar el servidor
CMD ["python", "-m", "app"] 