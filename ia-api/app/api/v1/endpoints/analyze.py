from app.services.analyzer import predict_from_bytes
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    image_bytes = await file.read()
    try:
        prediction = await predict_from_bytes(image_bytes)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
