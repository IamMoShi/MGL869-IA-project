from app.services.analyzer import analyze_image
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/")
async def analyze(file: UploadFile = File(...)):
    """

    Args:
        file: Upload file

    Returns: Result of the analysis

    """
    try:
        result = await analyze_image(file)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
