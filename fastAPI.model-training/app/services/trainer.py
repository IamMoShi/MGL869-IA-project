import logging
import os
import threading
import time

import albumentations as A
import pandas as pd
import timm
import torch
from app.core.minio import MODEL_BUCKET, PIPELINE_BUCKET, s3_client
from app.services.early_stopping import EarlyStopping
from app.services.load_dataset import ImageDatasetFromMinioDF
from app.services.log import clean_info_log
from app.core.metrics import training_metrics
from pydantic.v1 import BaseModel
from sklearn.model_selection import StratifiedKFold
from timm import optim
from torch import nn
from torch.utils.data import DataLoader

# Constants
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clean_info_log(f"Device used for training: {DEVICE}")
logger = logging.getLogger("uvicorn")


class TrainingParams(BaseModel):
    df_train: pd.DataFrame
    df_val: pd.DataFrame
    df_name: str
    model_name: str

    n_splits: int = 5
    max_epochs: int = 20
    batch_size: int = 32
    lr: float = 1e-4
    random_state: int = 42
    seed: int = 42
    weight_decay: float = 0.008835

    class Config:
        arbitrary_types_allowed = True


class Trainer:
    """A class responsible for managing the training process of an image
    classification model using k-fold cross-validation.

    It supports asynchronous execution, tracks metrics via Redis, and
    exposes real-time telemetry using OpenTelemetry.
    """

    def __init__(self):
        self._training_lock = threading.Lock()
        self.transform = A.Compose([A.Resize(224, 224), A.ToTensorV2()])

        training_metrics.set(0, {"metric": "training_in_progress"})
        training_metrics.set(0.0, {"metric": "training_progress"})

        training_metrics.set(0, {"metric": "current_epoch"})

        training_metrics.set(0.0, {"metric": "validation_loss"})
        training_metrics.set(0.0, {"metric": "validation_accuracy"})

        training_metrics.set(0.0, {"metric": "training_time"})
        training_metrics.set(0, {"metric": "epoch_time"})

    def start_training(self, params: TrainingParams):
        """Start the training process in a separate thread.

        :param params:
        :raises Exception: If a training session is already active.
        """
        if hasattr(self, "_training_lock") and self._training_lock.locked():
            raise Exception("A training session is already active.")

        thread = threading.Thread(target=self._train, args=(params,))
        thread.start()

    def _train(self, params: TrainingParams):
        with self._training_lock:
            training_time = time.time()
            training_metrics.set(1, {"metric": "training_in_progress"})

            train_df = params.df_train.reset_index(drop=True)
            val_df = params.df_val.reset_index(drop=True)

            model = timm.create_model(
                params.model_name, pretrained=True, num_classes=6
            )
            model.to(DEVICE)

            clean_info_log(f"Model created: {params.model_name}")

            train_dataset = ImageDatasetFromMinioDF(
                df=train_df,
                transform=self.transform,
                bucket=PIPELINE_BUCKET,
            )

            val_dataset = ImageDatasetFromMinioDF(
                df=val_df,
                transform=self.transform,
                bucket=PIPELINE_BUCKET,
            )

            train_loader = DataLoader(train_dataset, batch_size=params.batch_size, shuffle=True)
            val_loader = DataLoader(val_dataset, batch_size=params.batch_size, shuffle=False)

            optimizer = optim.Adam(
                model.parameters(),
                lr=params.lr,
                weight_decay=params.weight_decay,
            )

            criterion = nn.CrossEntropyLoss()
            early_stopping = EarlyStopping(patience=3)

            best_val_loss = float("inf")
            best_model_state = None

            for epoch in range(params.max_epochs):
                epoch_time = time.time()
                clean_info_log(f"Epoch {epoch + 1}/{params.max_epochs}")
                training_metrics.set(epoch + 1, {"metric": "current_epoch"})
                training_metrics.set(epoch / params.max_epochs, {"metric": "training_progress"})

                # TRAINING
                model.train()
                i = 0
                for images, labels in train_loader:
                    clean_info_log(f"batch number {i + 1} / {len(train_loader)}")
                    training_metrics.set(epoch / params.max_epochs + i / (len(train_loader) * params.max_epochs),
                                         {"metric": "training_progress"})

                    images, labels = images.to(DEVICE).float(), labels.to(DEVICE)
                    optimizer.zero_grad()
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    i += 1

                # VALIDATION
                model.eval()
                val_loss = 0.0
                val_correct = 0
                val_total = 0

                with torch.no_grad():
                    for images, labels in val_loader:
                        images, labels = images.to(DEVICE).float(), labels.to(DEVICE)
                        outputs = model(images)
                        loss = criterion(outputs, labels)
                        val_loss += loss.item() * images.size(0)
                        _, predicted = outputs.max(1)
                        val_correct += predicted.eq(labels).sum().item()
                        val_total += labels.size(0)

                val_loss /= val_total
                val_acc = val_correct / val_total

                training_metrics.set(time.time() - epoch_time, {"metric": "epoch_time"})
                training_metrics.set(val_loss, {"metric": "validation_loss"})
                training_metrics.set(val_acc, {"metric": "validation_accuracy"})

                clean_info_log(f"Validation loss: {val_loss:.4f}, accuracy: {val_acc:.4f}")

                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_model_state = model.state_dict()
                    clean_info_log(f"Validation improved, saving best model state...")

                early_stopping(val_loss)
                if early_stopping.early_stop:
                    clean_info_log("Early stopping triggered")
                    break

                # SAUVEGARDE DU MEILLEUR MODÈLE
            if best_model_state:
                clean_info_log("Saving best model to MinIO")
                self._save_model_to_minio(
                    model,
                    f"{params.model_name}.{params.df_name}.final",
                    best_model_state,
                    params.df_name,
                )

            training_metrics.set(1.0, {"metric": "training_progress"})
            training_metrics.set(time.time() - training_time, {"metric": "training_time"})

    def _save_model_to_minio(
            self, model: nn.Module, model_name: str, best_model_state: dict, df_name: str
    ):
        """Save the trained model to MinIO.

        :param model: The trained PyTorch model.
        :param model_name: The name of the model to be saved.
        """
        model_path = f"/tmp/{model_name}.pth"
        model_dir = os.path.dirname(model_path)

        # Ensure the parent directory exists
        os.makedirs(model_dir, exist_ok=True)

        model.load_state_dict(best_model_state)
        torch.save(model.state_dict(), model_path)

        s3_client.upload_file(
            model_path,
            MODEL_BUCKET,
            f"models/{df_name}/{model_name}.pth",
        )

        clean_info_log(f"Model {model_name} saved to MinIO")
