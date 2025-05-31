from app.api.v1.endpoints import health, train
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(train.router, tags=["train"])
