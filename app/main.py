from fastapi import FastAPI, Depends
from .api.deps import get_api_key
from sqlalchemy.orm import Session
from .core.database import get_db
from contextlib import asynccontextmanager
from app.core.database import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing database...")
    # builds the database tables
    Base.metadata.create_all(bind=engine)

    yield
    print("🛑 Shutting down...")


app = FastAPI(lifespan=lifespan, title="Pulse Metrics")


@app.get("/")
async def index():
    return {"message": "we are live @pulseMetric"}


@app.post("/users")
def create_user(db: Session = Depends(get_db)):
    return {"message": "Database is connected!"}



