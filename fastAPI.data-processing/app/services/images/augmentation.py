import io
import logging
import random
from datetime import datetime, timezone

import albumentations as al
import numpy as np
from app.core.minio import IMAGE_BUCKET, PIPELINE_BUCKET
from app.services.minio import get_image_from_minio, save_image_to_minio
from PIL import Image as PILImage

logger = logging.getLogger("uvicorn")


def build_directory_name(naming: str):
    """Function to create a new directory for augmented images.

    :return:
    """
    date: str = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    return f"{date}_{naming}"


def augment_images_from_minio(
    images: list[tuple[str, int]],
    n_aug_per_image: int = 1,
    naming: str = "weekly_augmented_images",
    train_ratio: float = 0.8,
):
    """Augment images from MinIO, split into train/test, and upload them back
    to MinIO.

    :param images: List of (filename, label) tuples.
    :param n_aug_per_image: Number of augmentations per image.
    :param naming: Directory name prefix.
    :param train_ratio: Ratio of data for training.
    """

    augment = al.Compose(
        [
            al.RandomResizedCrop((224, 224)),
            # al.HorizontalFlip(p=0.5),
            # al.Rotate(limit=15),
            # al.GaussNoise(std_range=(0.05, 0.15), p=0.3),
            # al.ColorJitter(p=0.5),
            # al.ToGray(p=0.1),
        ]
    )

    # Shuffle and split dataset
    random.shuffle(images)
    split_index = int(len(images) * train_ratio)
    train_images = images[:split_index]
    test_images = images[split_index:]

    directory_name = build_directory_name(naming)

    for subset, subset_images in [
        ("train", train_images),
        ("test", test_images),
    ]:
        for filename, label in subset_images:
            try:
                img = get_image_from_minio(key=filename, bucket=IMAGE_BUCKET)

                if isinstance(img, bytes):
                    img = PILImage.open(io.BytesIO(img)).convert("RGB")
                if isinstance(img, PILImage.Image):
                    img = np.array(img)

                for i in range(n_aug_per_image):
                    aug_img = augment(image=img)["image"]
                    aug_pil_img = PILImage.fromarray(aug_img)

                    key = f"{directory_name}/images/{subset}/{label}/{filename}_{i}.jpg"
                    save_image_to_minio(
                        image=aug_pil_img,
                        key=key,
                        bucket=PIPELINE_BUCKET,
                        img_format="JPEG",
                    )

            except Exception as e:
                error_message = str(e).replace("\n", "\\n")
                logger.error(f"Failed to augment {filename}: {error_message}")