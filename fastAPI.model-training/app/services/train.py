import time
from collections import defaultdict

import albumentations as al
import pandas as pd
import timm
import torch
from app.core.minio import PIPELINE_BUCKET, s3_client
from app.services.early_stopping import EarlyStopping
from app.services.load_dataset import ImageDatasetFromMinioDF
from sklearn.model_selection import StratifiedKFold
from timm import optim
from torch import nn
from torch.utils.data import DataLoader
from tqdm import tqdm

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train(
    model_name: str,
    df: pd.DataFrame,
    N_SPLITS: int = 5,
    MAX_EPOCHS: int = 20,
    BATCH_SIZE: int = 32,
    RANDOM_SEED: int = 42,
    PRETRAINED: bool = True,
    LR: float = 1e-4,
):
    NUM_CLASSES: int = df["label"].nunique()
    skf: StratifiedKFold = StratifiedKFold(
        n_splits=N_SPLITS, shuffle=True, random_state=42
    )
    transform: al.Compose = al.Compose([al.Resize(224, 224), al.ToTensorV2()])

    all_metrics = []

    for fold, (train_idx, val_idx) in enumerate(
        skf.split(df["image_path"], df["label"])
    ):
        train_df = df.iloc[train_idx].reset_index(drop=True)
        val_df = df.iloc[val_idx].reset_index(drop=True)

        model = timm.create_model(
            model_name,
            pretrained=PRETRAINED,
            num_classes=NUM_CLASSES,
        ).to(DEVICE)

        train_dataset = ImageDatasetFromMinioDF(
            df=train_df,
            s3_client=s3_client,
            bucket=PIPELINE_BUCKET,
            transform=transform,
        )

        val_dataset = ImageDatasetFromMinioDF(
            df=val_df,
            s3_client=s3_client,
            bucket=PIPELINE_BUCKET,
            transform=transform,
        )

        train_loader = DataLoader(
            train_dataset, batch_size=BATCH_SIZE, shuffle=True, drop_last=True
        )

        val_loader = DataLoader(
            val_dataset, batch_size=BATCH_SIZE, shuffle=False, drop_last=False
        )

        optimizer = optim.Adam(model.parameters(), lr=LR)
        criterion = nn.CrossEntropyLoss()
        early_stopper = EarlyStopping(patience=3)

        best_val_loss: float = float("inf")
        best_model_state = None

        fold_metrics = defaultdict(list)
        start_time = time.time()

        for epoch in range(MAX_EPOCHS):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in tqdm(
                train_loader,
                desc=f"Fold {fold+1} Epoch {epoch+1}/{MAX_EPOCHS}",
            ):
                images, labels = images.to(DEVICE), labels.to(DEVICE)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * images.size(0)
                _, predicted = outputs.max(1)
                correct += predicted.eq(labels).sum().item()
                total += labels.size(0)

            train_acc = correct / total
            train_loss = running_loss / total
            print(
                f"→ Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}"
            )

            # Validation
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

            val_loss /= val_total
            val_acc = val_correct / val_total
            print(f"→ Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")

            # Enregistrement des métriques
            fold_metrics["train_loss"].append(train_loss)
            fold_metrics["train_acc"].append(train_acc)
            fold_metrics["val_loss"].append(val_loss)
            fold_metrics["val_acc"].append(val_acc)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_model_state = model.state_dict()

            early_stopper(val_loss)
            if early_stopper.early_stop:
                print(f"🛑 Early stop at epoch {epoch+1}")
                break

        end_time = time.time()
        fold_metrics["epochs_done"] = epoch + 1
        fold_metrics["training_time_sec"] = end_time - start_time
        fold_metrics["best_val_loss"] = best_val_loss
        fold_metrics["best_val_acc"] = max(fold_metrics["val_acc"])

        all_metrics.append(fold_metrics)

        if best_model_state:
            model.load_state_dict(best_model_state)
            torch.save(
                model.state_dict(), f"{model_name}_fold{fold+1}_best.pth"
            )
            print(f"✅ Best model saved: {model_name}_fold{fold+1}_best.pth")
