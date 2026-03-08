"""FastAPI application entrypoint for Pulse Metric.

This module wires up:
- Application lifespan to initialize database schema at startup.
- API routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.models.base import Base
from app.api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    On startup:
    - Creates database tables from SQLAlchemy models if they do not exist yet.

    On shutdown:
    - Logs a simple shutdown message (hook for future cleanup if needed).
    """
    print("🚀 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("database ready 🦾...")

    yield

    print("🛑 Shutting down...")


app = FastAPI(lifespan=lifespan, title="Pulse Metrics")

# Register API routers
app.include_router(auth_router)


@app.get("/")
async def index():
    """Simple health-style endpoint to verify the API is running."""
    return {"message": "we are live @pulseMetric"}

