import time

import cv2
import optuna
import pandas as pd
import timm
import torch
import albumentations as A
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.model_selection import train_test_split
from collections import defaultdict

all_models = timm.list_models(["mobilenet*r224*", "resnet*r224*", ], pretrained=True)
print("-" + "\n-".join(all_models) + "\n", len(all_models))

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", DEVICE)


# Dataset for preprocessed image paths + labels
class ImageDatasetFromDF(Dataset):
    def __init__(self, df: pd.DataFrame, label_column="label", image_column="image_path", transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.image_column = image_column
        self.label_column = label_column

        # Encode string labels to integers
        self.label_to_index = {label: i for i, label in enumerate(sorted(df[label_column].unique()))}
        self.df["label_index"] = self.df[label_column].map(self.label_to_index)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img = cv2.imread(row[self.image_column])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label = row["label_index"]
        if self.transform:
            img = self.transform(image=img)["image"]
        img = img.float()
        return img, label


def objective_factory(model_name, df: pd.DataFrame, pretrained=True):
    def objective(trial):
        print("Optimizing with 5-Fold CV")

        # Sample hyperparameters
        lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
        weight_decay = trial.suggest_float("weight_decay", 1e-5, 1e-2)
        batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
        optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "SGD"])

        # Predefine transform
        transform = A.Compose([A.ToTensorV2()])

        # Encode labels
        label_to_index = {label: i for i, label in enumerate(sorted(df["label"].unique()))}
        df_local = df.copy()
        df_local["label_index"] = df_local["label"].map(label_to_index)

        # Cross-validation setup
        kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scores = []

        for fold_idx, (train_idx, val_idx) in enumerate(kf.split(df_local, df_local["label_index"])):
            print(f"\n📂 Fold {fold_idx + 1}/5")

            df_train = df_local.iloc[train_idx].reset_index(drop=True)
            df_val = df_local.iloc[val_idx].reset_index(drop=True)

            model = timm.create_model(model_name, pretrained=pretrained, num_classes=len(label_to_index))
            model = model.to(DEVICE)

            train_dataset = ImageDatasetFromDF(df_train, transform=transform)
            val_dataset = ImageDatasetFromDF(df_val, transform=transform)

            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
            val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, drop_last=True)

            optimizer_cls = getattr(optim, optimizer_name)
            optimizer = optimizer_cls(model.parameters(), lr=lr, weight_decay=weight_decay)
            criterion = nn.CrossEntropyLoss()

            n_epochs = 3
            for epoch in range(n_epochs):
                model.train()
                loop = tqdm(train_loader, desc=f"🧪 Fold {fold_idx + 1} | Epoch {epoch + 1}/{n_epochs}", leave=False)
                for images, labels in loop:
                    images, labels = images.float().to(DEVICE), labels.to(DEVICE)
                    optimizer.zero_grad()
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()

            model.eval()
            correct = total = 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.float().to(DEVICE), labels.to(DEVICE)
                    preds = model(images).argmax(dim=1)
                    correct += (preds == labels).sum().item()
                    total += labels.size(0)

            fold_acc = correct / total
            print(f"✅ Fold {fold_idx + 1} Accuracy: {fold_acc:.4f}")
            scores.append(fold_acc)

        mean_acc = np.mean(scores)
        return mean_acc

    return objective

class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None or val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True

def train(model_name):
    NUM_CLASSES = 6
    N_SPLITS = 5
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=42)

    transform = A.Compose([A.Resize(224, 224), A.ToTensorV2()])

    all_metrics = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(df['image_path'], df['label'])):
        print(f"\n🔁 Fold {fold + 1}/{N_SPLITS}")

        train_df = df.iloc[train_idx].reset_index(drop=True)
        val_df = df.iloc[val_idx].reset_index(drop=True)

        model = timm.create_model(model_name, pretrained=True, num_classes=NUM_CLASSES)
        model = model.to(DEVICE)

        train_dataset = ImageDatasetFromDF(train_df, transform=transform)
        val_dataset = ImageDatasetFromDF(val_df, transform=transform)

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, drop_last=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, drop_last=True)

        optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=0.008835)
        criterion = nn.CrossEntropyLoss()
        early_stopper = EarlyStopping(patience=3)

        EPOCHS = 50
        best_val_loss = float('inf')
        best_model_state = None

        # 💾 Initialisation métriques
        fold_metrics = defaultdict(list)
        start_time = time.time()

        for epoch in range(EPOCHS):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for images, labels in tqdm(train_loader, desc=f"Fold {fold+1} Epoch {epoch+1}/{EPOCHS}"):
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
            print(f"→ Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")

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

        # Sauvegarde du meilleur modèle de ce fold
        if best_model_state:
            model.load_state_dict(best_model_state)
            torch.save(model.state_dict(), f"{model_name}_fold{fold+1}_best.pth")
            print(f"✅ Best model saved: {model_name}_fold{fold+1}_best.pth")

    # 📊 Résumé global
    for i, m in enumerate(all_metrics):
        print(f"\n📄 Fold {i+1} Summary:")
        print(f"  ⏱️ Time: {m['training_time_sec']:.2f}s")
        print(f"  🔁 Epochs: {m['epochs_done']}")
        print(f"  🏆 Best Val Loss: {m['best_val_loss']:.4f}")
        print(f"  🥇 Best Val Acc: {m['best_val_acc']:.4f}")


if __name__ == "__main__":
    from dataset_file_manager import load

    df = load("datasets/augmented/images")
    print(df.head())

    # Launch Optuna for that model
    # study = optuna.create_study(direction="maximize")
    # study.optimize(objective_factory("mobilenetv4_conv_small.e2400_r224_in1k", df), n_trials=10)
    #
    # print("🏆 Best trial:", study.best_trial)

    # Train model
    train("mobilenetv4_conv_small.e2400_r224_in1k")
