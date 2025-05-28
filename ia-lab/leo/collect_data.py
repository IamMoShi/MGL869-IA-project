import os
import shutil
import random

import cv2
import kagglehub
import albumentations as A # Faster than torch for augmentations
import numpy as np


def download_dataset(destination_dir: str = "datasets/raw") -> None:
    print("Downloading data...")
    dataset_path = kagglehub.dataset_download("puneet6060/intel-image-classification")
    print("Download complete. Moving to destination directory...")
    shutil.copytree(dataset_path, destination_dir, dirs_exist_ok=True)
    print(f"Dataset copied to {destination_dir}")


def restructure_raw_dataset(path: str = "datasets/raw", new_path: str = "datasets/restructured") -> None:
    """
    Restructures the raw dataset to have a consistent directory structure.
    :param path: The root location of the dataset.
    :param new_path: The destination directory for the restructured dataset.
    :return: None
    """

    # Define the new structure
    new_structure = {
        "images": ["seg_train/seg_train", "seg_test/seg_test"],
    }

    os.makedirs(new_path, exist_ok=True)

    for split, subdirs in new_structure.items():
        for subdir in subdirs:
            src = os.path.join(path, subdir)
            dst = os.path.join(new_path, split)

            os.makedirs(dst, exist_ok=True)

            # Move files to the new directory
            for label in os.listdir(src):
                label_dir = os.path.join(src, label)
                if os.path.isdir(label_dir):
                    dst_label_dir = os.path.join(dst, label)
                    if os.path.exists(dst_label_dir):
                        # Merge contents if the destination directory already exists
                        for item in os.listdir(label_dir):
                            shutil.move(os.path.join(label_dir, item), dst_label_dir)
                    else:
                        shutil.move(label_dir, dst)


def augment_dataset(df, n_aug_per_image=3, seed=42, output_dir="augmented_output") -> None:
    """
    Applies data augmentation to each image in the dataframe and saves them to the specified path.
    Args:
        df (pd.DataFrame): Dataframe with original images and labels
        n_aug_per_image (int): Number of augmented versions per image
        output_dir (str): Base output directory for augmented images
    Returns:
        None
    """
    print("Augmenting data...")
    np.random.seed(seed)
    random.seed(seed)

    # Define your augmentation pipeline here
    augment = A.Compose([
        A.RandomResizedCrop((224, 224)),          # Random crop + resize
        A.HorizontalFlip(p=0.5),                  # Flip horizontally with 50% chance
        A.Rotate(limit=15),                       # Rotate image within ±15°
        A.GaussNoise(std_range=(0.05, 0.15), mean_range=(0.0, 0.0), per_channel=True, p=0.3),  # Add Gaussian noise with 30% chance
        A.ColorJitter(p=0.5),                     # Adjust brightness/contrast/colors
        A.ToGray(p=0.1),                          # Convert to grayscale with 10% chance
    ])


    # Create the base output directory
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    for _, row in df.iterrows():
        img_path = row["image_path"]
        label = row["label"]

        # Create a subdirectory for each label
        label_dir = os.path.join(images_dir, label)
        os.makedirs(label_dir, exist_ok=True)

        img = cv2.imread(img_path)
        if img is None:
            continue  # Skip corrupted or unreadable images
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for i in range(n_aug_per_image):
            # Apply augmentation
            augmented_img = augment(image=img)["image"]

            # Save the augmented image
            filename = f"aug_{os.path.splitext(os.path.basename(img_path))[0]}_{i:03d}.jpg"
            output_path = os.path.join(label_dir, filename)
            cv2.imwrite(output_path, cv2.cvtColor(augmented_img, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    # Download the dataset
    download_dataset()

    # Restructure the dataset
    restructure_raw_dataset()

    # load the dataset
    from dataset_file_manager import load
    df_restructured = load("datasets/restructured/images")

    # Augment the dataset
    augment_dataset(df_restructured, n_aug_per_image=3, output_dir="datasets/augmented")
