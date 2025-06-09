import os
import threading

import boto3
from tqdm import tqdm


class ProgressPercentage:
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self._tqdm = tqdm(
            total=self._size, unit="B", unit_scale=True, desc=filename
        )

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self._tqdm.update(bytes_amount)
            if self._seen_so_far >= self._size:
                self._tqdm.close()


# --- Configuration MinIO
endpoint = "http://localhost:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "training-data"
folder_path = "datasets/base-dataset"
prefix_in_bucket = "/base-dataset"

s3_client = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# --- Lister tous les fichiers et leur taille totale
all_files = []
total_size = 0
for root, _, files in os.walk(folder_path):
    for filename in files:
        local_path = os.path.join(root, filename)
        relative_path = os.path.relpath(local_path, folder_path)
        s3_key = os.path.join(prefix_in_bucket, relative_path).replace(
            "\\", "/"
        )
        size = os.path.getsize(local_path)
        total_size += size
        all_files.append((local_path, s3_key, size))

# --- Barre de progression globale
with tqdm(
    total=total_size, unit="B", unit_scale=True, desc="Uploading folder"
) as pbar:
    for local_path, s3_key, size in all_files:

        def progress_callback(bytes_transferred, size=size):
            pbar.update(min(bytes_transferred, size))  # Évite de dépasser

        s3_client.upload_file(
            Filename=local_path,
            Bucket=bucket_name,
            Key=s3_key,
            Callback=progress_callback,
        )
