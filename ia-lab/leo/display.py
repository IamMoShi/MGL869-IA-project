import matplotlib.pyplot as plt
import cv2
import pandas as pd


def show_category_representatives(df: pd.DataFrame, image_column="image_path", label_column="label", n_per_class=5):
    """
    Displays n representative images per class from a DataFrame of image paths.

    Args:
        df (pd.DataFrame): DataFrame with image paths and labels
        image_column (str): Column name containing image file paths
        label_column (str): Column name containing class labels
        n_per_class (int): Number of images to show per class
    """
    unique_labels = sorted(df[label_column].unique())

    for label in unique_labels:
        subset = df[df[label_column] == label].head(n_per_class)

        fig, axes = plt.subplots(1, len(subset), figsize=(15, 3))
        fig.suptitle(f"Class: {label}", fontsize=14)

        for ax, (_, row) in zip(axes, subset.iterrows()):
            img = cv2.imread(row[image_column])
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img)
            ax.axis('off')

        plt.tight_layout()
        plt.show()
