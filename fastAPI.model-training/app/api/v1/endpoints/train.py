import logging

from app.services.load_dataset import load_dataset_from_minio
from app.services.trainer import Trainer
from fastapi import APIRouter

logger = logging.getLogger("uvicorn")
router = APIRouter()
trainer = Trainer()


@router.post("/train")
def launch_training():
    df_train, df_test = load_dataset_from_minio(
        "2025-05-29-00-48-44_last1000_random500"
    )
    trainer.start_training(df_train, MAX_EPOCHS=5)
    return {"message": "Training started"}


@router.get("/status")
def status():
    return trainer.get_status()


@router.get("/metrics")
def metrics():
    return trainer.get_metrics()
