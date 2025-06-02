import logging

from app.services.load_dataset import load_dataset_from_minio
from app.services.trainer import Trainer, TrainingParams
from fastapi import APIRouter

logger = logging.getLogger("uvicorn")
router = APIRouter()
trainer = Trainer()


@router.post("/train")
def launch_training():
    df_train, df_test = load_dataset_from_minio(
        "2025-06-01-02-10-34_last1000_random500"
    )
    trainer.start_training(
        TrainingParams(
            df=df_train,
            df_name="2025-06-01-02-10-34_last1000_random500",
            model_name="resnet50",
            n_splits=5,
            max_epochs=50,
            batch_size=32,
            lr=1e-4,
            seed=42,
        )
    )

    return {"message": "Training started"}
