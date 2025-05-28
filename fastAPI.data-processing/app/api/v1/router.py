from app.api.v1.endpoints import health, process
from fastapi import APIRouter, logger

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(process.router, tags=["process"])
