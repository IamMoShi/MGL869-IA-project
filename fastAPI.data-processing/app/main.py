from app.api.v1.router import router as v1_router
from app.core.database import engine
from app.models import image
from app.models.base import Base
from fastapi import FastAPI

app = FastAPI(title="Data Processing API", version="0.0.1")
app.include_router(v1_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    import app.models.image

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
