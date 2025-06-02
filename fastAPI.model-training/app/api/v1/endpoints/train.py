import logging

from app.services.load_dataset import load_dataset_from_minio
from app.services.trainer import Trainer, TrainingParams
from fastapi import APIRouter, Query

logger = logging.getLogger("uvicorn")
router = APIRouter()
trainer = Trainer()


@router.get("/train")
def launch_training(df_name: str = Query(...)):
    # Check if df_name is provided
    if not df_name:
        logger.error("No dataset name provided for training.")
        return {"error": "Dataset name must be provided."}
    df_train, df_test = load_dataset_from_minio(df_name)

    try:
        trainer.start_training(
            TrainingParams(
                df=df_train,
                df_name=df_name,
                model_name="mobilenetv4_conv_small.e2400_r224_in1k",
                n_splits=5,
                max_epochs=50,
                batch_size=32,
                lr=1e-4,
                seed=42,
            )
        )
    except Exception as e:
        logger.error(f"Error during training: {e}")
        return {"error": str(e)}
    return {"message": "Training started"}
