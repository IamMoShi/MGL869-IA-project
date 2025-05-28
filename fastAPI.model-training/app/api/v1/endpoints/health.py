from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check():
    """
    Returns health information
    Returns: TODO - Improve health check

    """
    return {"status": "ok"}
