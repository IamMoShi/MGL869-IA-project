from app.api.v1.endpoints import health
from fastapi import APIRouter

router = APIRouter()
router.include_router(health.router, tags=["health"])
