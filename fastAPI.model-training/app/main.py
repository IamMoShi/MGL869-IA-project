from app.api.v1.router import router as v1_router
from fastapi import FastAPI

app = FastAPI(title="Model Training API", version="0.0.1")
app.include_router(v1_router, prefix="/api/v1")
