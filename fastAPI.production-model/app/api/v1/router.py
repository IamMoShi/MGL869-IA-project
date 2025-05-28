from app.api.v1.endpoints import analyze, health
from fastapi import APIRouter

router = APIRouter()
router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
router.include_router(health.router, tags=["health"])
