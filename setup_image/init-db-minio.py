import os
import random
from datetime import datetime, timedelta

import boto3
import requests
from models.image import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Configuration ---
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "images"
DB_URL = "postgresql://postgres:changeme@localhost:5432/web-database"
IMAGES_DIR = "./images"
ANALYZE_API_URL = "http://127.0.0.1:5000/api/v1/analyze/predict"
PROGRESS_EVERY = 100

CLASS_MAP = {
    "buildings": 0,
    "forest": 1,
    "glacier": 2,
    "mountain": 3,
    "sea": 4,
    "street": 5,
}

# --- Setup MinIO & DB ---
s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)
# engine = create_engine(DB_URL)
# Session = sessionmaker(bind=engine)
# session = Session()


def random_date_within_last_two_months():
    now = datetime.utcnow()
    return now - timedelta(
        days=random.randint(0, 60),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


# --- Traitement ---docker ps
filenames = [
    f
    for f in os.listdir(IMAGES_DIR)
    if os.path.isfile(os.path.join(IMAGES_DIR, f))
]
total = len(filenames)
errors = 0

for idx, filename in enumerate(filenames, start=1):
    filepath = os.path.join(IMAGES_DIR, filename)

    try:
        s3.upload_file(filepath, MINIO_BUCKET, filename)
        created_at = random_date_within_last_two_months()

        if random.random() < 0.1:
            attribution_method = 1
            category = random.randint(0, 5)
        else:
            with open(filepath, "rb") as img_file:
                resp = requests.post(
                    ANALYZE_API_URL,
                    files={"file": (filename, img_file, "image/jpeg")},
                )
                resp.raise_for_status()
                label = resp.json()["prediction"]
                category = CLASS_MAP[label]
            attribution_method = 0

        # image = Image(
        #     filename=filename,
        #     category=category,
        #     attribution_method=attribution_method,
        #     created_at=created_at,
        # )
        # session.add(image)

    except Exception as e:
        errors += 1
        print(f"[{idx}/{total}] ❌ {filename} : {e}")

    if idx % PROGRESS_EVERY == 0:
        print(f"[{idx}/{total}] Progress...")

# session.commit()
print(f"✅ Upload terminé : {total - errors} réussis, {errors} erreurs.")
