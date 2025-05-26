import io

from app.services.analyzer import predict_from_bytes
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from app.core.minio import s3_client, BUCKET_NAME

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

@router.get("/image/{filename}")
def get_image(filename: str):
    try:
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        content_type = s3_object["ContentType"] if "ContentType" in s3_object else "image/jpeg"
        return StreamingResponse(
            io.BytesIO(s3_object["Body"].read()),
            media_type=content_type
        )
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))