from fastapi import FastAPI
from fastapi import Depends
from .api.deps import get_api_key


app = FastAPI(title="Pulse Metrics")

@app.get("/")
async def index():
    return {"message": "we are live @pulseMetric"}

