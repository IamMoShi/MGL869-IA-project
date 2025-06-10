import os
import cv2
import shutil
from tqdm import tqdm

SOURCE_DIR = "images_raw"
OUT_LOW = "texture_low"
OUT_MEDIUM = "texture_medium"
OUT_HIGH = "texture_high"

# Seuils ajustables : plus c’est haut, plus c’est "texturé"
THRESHOLD_LOW = 800
THRESHOLD_HIGH = 3500

# Crée les dossiers de sortie
os.makedirs(OUT_LOW, exist_ok=True)
os.makedirs(OUT_MEDIUM, exist_ok=True)
os.makedirs(OUT_HIGH, exist_ok=True)

def texture_score(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Image non lisible : {image_path}")
    return cv2.Laplacian(image, cv2.CV_64F).var()

filenames = [
    f for f in os.listdir(SOURCE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

for f in tqdm(filenames):
    path = os.path.join(SOURCE_DIR, f)
    try:
        score = texture_score(path)
        if score < THRESHOLD_LOW:
            shutil.copy2(path, os.path.join(OUT_LOW, f))
        elif score < THRESHOLD_HIGH:
            shutil.copy2(path, os.path.join(OUT_MEDIUM, f))
        else:
            shutil.copy2(path, os.path.join(OUT_HIGH, f))
    except Exception as e:
        print(f"❌ Erreur sur {f} : {e}")

print("✅ Tri par texture terminé.")
