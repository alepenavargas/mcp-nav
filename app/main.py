"""Aplicación principal."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import user

app = FastAPI(
    title="User Management API",
    description="API para gestión de usuarios",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(user.router)

@app.get("/")
async def root():
    """Endpoint raíz."""
    return {"message": "User Management API"} 