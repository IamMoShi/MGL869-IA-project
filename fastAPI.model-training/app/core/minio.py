import os

import boto3

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
IMAGE_BUCKET = os.getenv("BUCKET_NAME", "images")
PIPELINE_BUCKET = os.getenv("PIPELINE_BUCKET", "training-data")
MODEL_BUCKET = os.getenv("MODEL_BUCKET", "models")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)
