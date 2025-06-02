from aiocache import SimpleMemoryCache, cached
from app.core.minio import BUCKET_NAME, s3_client
from app.services.analyzer import predict_from_bytes, MODEL_VERSION
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.metrics import inferences_counter, inference_latence_gauge, inference_avg_latence_gauge
from app.logger import logger, makeMessage, CODE_SUCCESS, CODE_ERROR

import time

source="fastAPI.production-model"

router = APIRouter()

latency_average = 0.0
predictions_counter = 0

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    image_bytes = await file.read()
    try:
        global latency_average
        global predictions_counter

        predictions_counter += 1
        logger.info(makeMessage(errorType=CODE_SUCCESS, sourceService=source, apiEndpoint="/predict", model_version=MODEL_VERSION, val1=predictions_counter, val2=file.filename, message=f"Total predictions: {predictions_counter}"))

        inferences_counter.add(1, {"metric": "inferences_count"})

        start_time = time.time()
        prediction = await predict_from_bytes(image_bytes)
        elapsed_time = time.time() - start_time
        logger.info(makeMessage(errorType=CODE_SUCCESS, sourceService=source, apiEndpoint="/predict", model_version=MODEL_VERSION, val1=prediction, val2=file.filename, message=f"Prediction: {prediction}, Latency: {elapsed_time:.2f} seconds"))

        inference_latence_gauge.set(elapsed_time, {"metric": "latence"})
        if predictions_counter == 1:
            latency_average = elapsed_time
        else:
            latency_average = (latency_average + elapsed_time) / 2
        inference_avg_latence_gauge.set(latency_average, {"metric": "average_latence"})
        
        latency_average= round(latency_average, 2)
        logger.info(makeMessage(errorType=CODE_SUCCESS, sourceService=source, apiEndpoint="/predict", model_version=MODEL_VERSION, val1=latency_average, val2=file.filename, message=f"Average latency: {latency_average} seconds"))

        return {"prediction": prediction}
    
    except Exception as e:
        logger.error(makeMessage(errorType=CODE_ERROR, sourceService=source, apiEndpoint="/predict", model_version=MODEL_VERSION, val1="", val2=file.filename, message=f"An exception occurred while predicting the class of an image."))
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
        start_time = time.time()
        prediction = await get_prediction_from_s3(filename)
        elapsed_time = time.time() - start_time
        logger.info(makeMessage(errorType=CODE_SUCCESS, sourceService=source, apiEndpoint="/image/{filename}", model_version=MODEL_VERSION, val1=prediction, val2=filename, message=f"Prediction: {prediction}, Latency: {elapsed_time:.2f} seconds"))
        return {"filename": filename, "prediction": prediction}
    
    except s3_client.exceptions.NoSuchKey:
        logger.error(makeMessage(errorType=CODE_ERROR, sourceService=source, apiEndpoint="/image/{filename}", model_version=MODEL_VERSION, val1="", val2=filename, message=f"An exception occurred while retrieving the image: {filename}"))
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        logger.error(makeMessage(errorType=CODE_ERROR, sourceService=source, apiEndpoint="/image/{filename}", model_version=MODEL_VERSION, val1="", val2=filename, message=f"An exception occurred : {str(e)}"))
        raise HTTPException(status_code=500, detail=str(e))
