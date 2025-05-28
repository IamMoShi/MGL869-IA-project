import os
from glob import glob

import pandas as pd


def load(path: str) -> pd.DataFrame:
    """Loads images from directories in a DataFrame.

    :param path: Directory containing the images
    :return:
    """

    # Check if the path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path {path} does not exist.")

    # Initialize an empty list to store image paths and labels
    data = []

    # Iterate through each subdirectory (label)
    for label in os.listdir(path):
        label_dir = os.path.join(path, label)

        if os.path.isdir(label_dir):
            # Iterate through each image in the subdirectory

            for img_path in glob(os.path.join(label_dir, "*")):
                if img_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    data.append({"image_path": img_path, "label": label})

    # Create a DataFrame from the list
    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    # Example usage
    df = load("datasets/raw/seg_train/seg_train")
    print(df.head())
