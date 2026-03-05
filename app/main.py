from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine
from app.models.base import Base
from app.api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing database...")
    # builds the database tables
    Base.metadata.create_all(bind=engine)
    print("database ready 🦾...")

    yield
    print("🛑 Shutting down...")


app = FastAPI(lifespan=lifespan, title="Pulse Metrics")


# Mount the router
app.include_router(auth_router)

@app.get("/")
async def index():
    return {"message": "we are live @pulseMetric"}

