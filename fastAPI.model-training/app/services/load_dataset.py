import logging

import boto3
import cv2
import numpy as np
import pandas as pd
import torch
from app.core.minio import PIPELINE_BUCKET, s3_client
from app.services.log import clean_info_log
from PIL import Image
from torch.utils.data import Dataset


def load_dataset_from_minio(repertory: str):
    clean_info_log(f"Loading dataset from {repertory}")
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

    clean_info_log("Loading dataset completed")

    return dict_to_df(dataset_train, "train"), dict_to_df(dataset_test, "test")


class ImageDatasetFromMinioDF(Dataset):
    def __init__(
        self, df: pd.DataFrame, bucket, transform, label_column="label"
    ):
        self.df = df
        self.s3_client = s3_client
        self.bucket_name = bucket
        self.transform = transform
        self.label_column = label_column

        if self.label_column not in df.columns:
            raise KeyError(
                f"Column '{self.label_column}' not found in DataFrame"
            )

        self.label_map = {
            label: i
            for i, label in enumerate(sorted(df[self.label_column].unique()))
        }

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image_path = row["image_path"]
        label = self.label_map[row[self.label_column]]

        # Download image from MinIO
        response = self.s3_client.get_object(
            Bucket=self.bucket_name, Key=image_path
        )
        image = Image.open(response["Body"]).convert("RGB")
        image = np.array(image)

        # Apply transformations
        image = self.transform(image=image)["image"]

        return image, label
