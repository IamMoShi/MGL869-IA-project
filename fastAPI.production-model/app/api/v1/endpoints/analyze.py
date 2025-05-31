from aiocache import SimpleMemoryCache, cached
from app.core.minio import BUCKET_NAME, s3_client
from app.services.analyzer import predict_from_bytes
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.metrics import inferences_counter, inference_latence_gauge
import time

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    image_bytes = await file.read()
    try:
        start_time = time.time()
        prediction = await predict_from_bytes(image_bytes)
        elapsed_time = time.time() - start_time
        inference_latence_gauge.set(elapsed_time, {"metric": "latence"})
        print(f"Prediction: {prediction}, Latency: {elapsed_time:.2f} seconds")
        inferences_counter.add(1, {"metric": "inferences_count"})
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@cached(
    ttl=3600, cache=SimpleMemoryCache
)  # Can be updated to use RedisCache or another cache for distributed caching
async def get_prediction_from_s3(filename: str):
    s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    image_bytes = s3_object["Body"].read()
    return await predict_from_bytes(image_bytes)


@router.get("/image/{filename}")
async def analyze_image(filename: str):
    try:
        prediction = await get_prediction_from_s3(filename)
        return {"filename": filename, "prediction": prediction}
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
