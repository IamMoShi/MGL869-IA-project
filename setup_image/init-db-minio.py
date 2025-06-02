import os
import random
from datetime import datetime, timedelta

import boto3
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
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()


def random_date_within_last_two_months():
    now = datetime.utcnow()
    return now - timedelta(
        days=random.randint(0, 60),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


# --- Traitement ---
errors = 0
total = 0

for class_name, class_id in CLASS_MAP.items():
    class_dir = os.path.join(IMAGES_DIR, class_name)
    if not os.path.isdir(class_dir):
        print(f"⚠️ Dossier manquant : {class_dir}")
        continue

    filenames = [
        f
        for f in os.listdir(class_dir)
        if os.path.isfile(os.path.join(class_dir, f))
    ]

    for filename in filenames:
        total += 1
        filepath = os.path.join(class_dir, filename)

        try:
            # Envoi à la racine du bucket (clé = nom du fichier uniquement)
            s3.upload_file(filepath, MINIO_BUCKET, filename)

            created_at = random_date_within_last_two_months()

            image = Image(
                filename=filename,  # Clé simple (sans dossier)
                category=class_id,
                attribution_method=1,  # Dérivé de la structure du dossier
                created_at=created_at,
            )
            session.add(image)

        except Exception as e:
            errors += 1
            print(f"[{total}] ❌ {filename} : {e}")

        if total % PROGRESS_EVERY == 0:
            print(f"[{total}] Progress...")

session.commit()
print(f"✅ Upload terminé : {total - errors} réussis, {errors} erreurs.")
