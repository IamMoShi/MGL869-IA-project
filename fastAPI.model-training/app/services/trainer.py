import json
import threading
import time

import albumentations as al
import pandas as pd
import redis
import timm
import torch
from app.core.minio import PIPELINE_BUCKET, s3_client
from app.services.early_stopping import EarlyStopping
from app.services.load_dataset import ImageDatasetFromMinioDF
from sklearn.model_selection import StratifiedKFold
from timm import optim
from torch import nn
from torch.utils.data import DataLoader

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Trainer:
    def __init__(self):
        self.redis = redis_client
        self.transform = al.Compose([al.Resize(224, 224), al.ToTensorV2()])

    def start_training(self, df: pd.DataFrame, **kwargs):
        if self.redis.get("trainer:lock") == "1":
            raise Exception("Trainer already in progress")

        self.redis.set("trainer:lock", "1")
        self.redis.delete("trainer:metrics")

        thread = threading.Thread(
            target=self._train, args=(df,), kwargs=kwargs
        )
        thread.start()

    def _train(self, df: pd.DataFrame, **kwargs):
        t = time.time()
        try:
            max_epochs = kwargs.get("MAX_EPOCHS", 10)

            for epoch in range(max_epochs):
                # Dummy metrics
                status = {
                    "epoch": epoch + 1,
                    "train_loss": round(1.0 / (epoch + 1), 4),
                    "val_loss": round(1.2 / (epoch + 1), 4),
                }

                self.redis.set("trainer:status", json.dumps(status))
                self.redis.rpush("trainer:metrics", json.dumps(status))

                time.sleep(1)
        finally:
            self.redis.set("trainer:lock", "0")
            print(time.time() - t)

    def _train_kfold(self, df: pd.DataFrame, **kwargs):

        n_split: int = kwargs.get("N_SPLITS", 5)
        random_state: int = kwargs.get("random_state", 42)
        model_name: str = kwargs.get(
            "model", "mobilenetv4_conv_small.e2400_r224_in1k"
        )
        batch_size: int = kwargs.get("batch_size", 32)
        lr: float = kwargs.get("lr", 1e-4)

        skf: StratifiedKFold = StratifiedKFold(
            n_splits=n_split, shuffle=True, random_state=random_state
        )

        for fold, (train_idx, val_idx) in enumerate(
            skf.split(df["image_path"], df["label"])
        ):
            train_df = df.iloc[train_idx].reset_index(drop=True)
            val_df = df.iloc[val_idx].reset_index(drop=True)
            model = timm.create_model(
                model_name,
                pretrained=True,
                num_classes=6,
            ).to(DEVICE)

            train_dataset = ImageDatasetFromMinioDF(
                df=train_df,
                s3_client=s3_client,
                bucket=PIPELINE_BUCKET,
                transform=self.transform,
            )

            val_dataset = ImageDatasetFromMinioDF(
                df=val_df,
                s3_client=s3_client,
                bucket=PIPELINE_BUCKET,
                transform=self.transform,
            )

            train_loader = DataLoader(
                train_dataset,
                batch_size=batch_size,
                shuffle=True,
                drop_last=True,
            )

            val_loader = DataLoader(
                val_dataset,
                batch_size=batch_size,
                shuffle=False,
                drop_last=False,
            )

            optimizer = optim.Adam(model.parameters(), lr=lr)
            criterion = nn.CrossEntropyLoss()
            early_stopper = EarlyStopping(patience=3)

            best_val_loss: float = float("inf")
            best_model_state = None

    def _train_epoch(
        self,
        model,
        train_loader,
        optimizer,
        criterion,
        best_val_loss,
        val_loader,
    ):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            # Move data to the appropriate device
            images, labels = images.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()  # Reset gradients
            outputs = model(images)  # Forward pass
            loss = criterion(outputs, labels)  # Compute loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update weights

            running_loss += loss.item() * images.size(0)  # Accumulate loss
            _, predicted = torch.max(outputs, 1)  # Get predictions
            correct += (
                predicted.eq(labels).sum().item()
            )  # Count correct predictions
            total += labels.size(0)

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(DEVICE), labels.to(DEVICE)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                val_correct += predicted.eq(labels).sum().item()
                val_total += labels.size(0)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_model_state = model.state_dict()

    def get_status(self):
        raw = self.redis.get("trainer:status")
        return json.loads(raw) if raw else {}

    def get_metrics(self):
        return [
            json.loads(v) for v in self.redis.lrange("trainer:metrics", 0, -1)
        ]
