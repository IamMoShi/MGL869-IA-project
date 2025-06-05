import logging

import pandas as pd
from sklearn.model_selection import train_test_split

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
    df_train_base, df_test_base = load_dataset_from_minio("base-dataset")

    # Afficher la taille des DataFrames
    logger.info(f"Training DataFrame shape: {df_train.shape}")
    logger.info(f"Test DataFrame shape: {df_test.shape}")
    logger.info(f"Base Training DataFrame shape: {df_train_base.shape}")
    logger.info(f"Base Test DataFrame shape: {df_test_base.shape}")

    # Fusionner les deux DataFrames

    df_train = pd.concat([df_train, df_train_base], ignore_index=True)
    df_test = pd.concat([df_test, df_test_base], ignore_index=True)

    df_train, df_val = train_test_split(
        df_train,
        test_size=0.2,  # 20% pour validation
        stratify=df_train["label"],  # pour garder le même équilibre de classes
        random_state=42  # pour que le split soit reproductible
    )
    try:
        trainer.start_training(
            TrainingParams(
                df_train=df_train,
                df_val=df_val,
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
