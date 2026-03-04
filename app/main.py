from fastapi import FastAPI
from fastapi import Depends
from .api.deps import get_api_key
from sqlalchemy.orm import Session
from .core.database import get_db


app = FastAPI(title="Pulse Metrics")

@app.get("/")
async def index():
    return {"message": "we are live @pulseMetric"}


@app.post("/users")
def create_user(db: Session = Depends(get_db)):
    return {"message": "Database is connected!"}
    