from app.services.early_stopping import EarlyStopping
import pandas as pd
from app.services.train import train
from sklearn.model_selection import StratifiedKFold
import timm
import torch
import pytest
import torch.nn as nn
from torch.utils.data import Dataset
from app import services

def test_stratified_split_label_balance():
    import pandas as pd

    df = pd.DataFrame({
        "image_path": [f"img_{i}.jpg" for i in range(100)],
        "label": [i % 5 for i in range(100)]
    })

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for train_idx, val_idx in skf.split(df["image_path"], df["label"]):
        train_labels = df.iloc[train_idx]["label"].value_counts()
        val_labels = df.iloc[val_idx]["label"].value_counts()
        assert set(train_labels.keys()) == set(val_labels.keys())

def test_model_instantiation():
    model = timm.create_model("resnet18", pretrained=False, num_classes=10)
    assert model is not None



def test_early_stopping():
    early_stopper = EarlyStopping(patience=2)
    losses = [1.0, 0.9, 0.91, 0.92]  # le modèle se dégrade après epoch 1

    for loss in losses:
        early_stopper(loss)
        if early_stopper.early_stop:
            break

    assert early_stopper.early_stop is True

# Dummy Dataset
class DummyDataset(Dataset):
    def __init__(self, df, bucket=None, transform=None, label_column="label"):
        self.df = df
        self.transform = transform
        self.label_column = label_column
        self.label_map = {label: i for i, label in enumerate(sorted(df[self.label_column].unique()))}

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Renvoie un tensor aléatoire et un label basé sur le DataFrame
        image = torch.randn(3, 224, 224)
        label = self.label_map[self.df.iloc[idx][self.label_column]]
        return image, label


# Dummy modèle
class DummyModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.fc = nn.Linear(150528, num_classes)  # 3x224x224 aplati

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.fc(x)


# Patch de timm.create_model et du Dataset
@pytest.fixture
def monkeypatch_train(monkeypatch):
    def dummy_create_model(model_name, pretrained, num_classes):
        return DummyModel(num_classes)

    monkeypatch.setattr(services.train.timm, "create_model", dummy_create_model)
    monkeypatch.setattr(services.train, "ImageDatasetFromMinioDF", DummyDataset)


def test_train_outputs_metrics(monkeypatch_train):
    # Création d’un DataFrame factice avec 10 images et 2 classes
    df = pd.DataFrame({
        "image_path": [f"img_{i}.jpg" for i in range(10)],
        "label": [i % 2 for i in range(10)],
    })

    metrics = train(
        model_name="dummy_model",
        df=df,
        N_SPLITS=2,
        MAX_EPOCHS=1,
        BATCH_SIZE=2,
        RANDOM_SEED=42,
        PRETRAINED=False,
        LR=1e-3,
    )

    assert isinstance(metrics, list)
    assert len(metrics) == 2  # 2 folds
    for fold_metrics in metrics:
        assert "train_loss" in fold_metrics
        assert "val_loss" in fold_metrics
        assert "best_val_acc" in fold_metrics
