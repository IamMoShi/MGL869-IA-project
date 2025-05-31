import boto3
import cv2
import numpy as np
import pandas as pd
from app.core.minio import PIPELINE_BUCKET, s3_client
from torch.utils.data import Dataset


def load_dataset_from_minio(repertory: str):
    paginator = s3_client.get_paginator("list_objects_v2")

    def get_subset(subset: str):
        NUM_CLASSES: int = 6
        prefix: str = repertory + "/images/" + subset
        subset_images = {i: [] for i in range(NUM_CLASSES)}
        for label in range(NUM_CLASSES):
            page_iterator = paginator.paginate(
                Bucket=PIPELINE_BUCKET, Prefix=prefix + f"/{label}/"
            )
            for page in page_iterator:
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    if key.lower().endswith((".jpg", ".jpeg", ".png")):
                        subset_images[label].append(key)
        return subset_images

    dataset_train = get_subset("train")
    dataset_test = get_subset("test")

    def dict_to_df(data: dict[int, list[str]], split: str) -> pd.DataFrame:
        df = (
            pd.DataFrame.from_dict(data, orient="index")
            .transpose()
            .melt(var_name="label", value_name="image_path")
            .dropna()
        )
        df["split"] = split
        return df

    return dict_to_df(dataset_train, "train"), dict_to_df(dataset_test, "test")


class ImageDatasetFromMinioDF(Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        s3_client: boto3.client,
        bucket: str,
        label_column="label",
        image_column="image_path",
        transform=None,
    ):
        self.df = df.reset_index(drop=True)
        self.s3_client = s3_client
        self.bucket = bucket
        self.transform = transform
        self.image_column = image_column
        self.label_column = label_column

        # Encode string labels to integers
        self.label_to_index = {
            label: i
            for i, label in enumerate(sorted(df[label_column].unique()))
        }
        self.df["label_index"] = self.df[label_column].map(self.label_to_index)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        key = row[self.image_column]

        # Download the image from Minio
        s3_obj = self.s3_client.get_object(Bucket=self.bucket, Key=key)
        image_bytes = s3_obj["Body"].read()

        # Convert to table numpy via OpenCV
        img_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Transformation
        if self.transform:
            img = self.transform(image=img)["image"]

        # Float tensor (PyTorch)
        img = img.float()
        label = row["label_index"]
        return img, label
