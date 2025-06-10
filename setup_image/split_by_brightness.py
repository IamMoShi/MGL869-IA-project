import os
import cv2
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt

SOURCE_DIR = "images_raw"

# Seuils
THRESHOLDS = [90, 120, 150]
OUTPUT_DIRS = [
    "brightness_very_low",
    "brightness_low",
    "brightness_medium",
    "brightness_high",
]

# Créer les dossiers de sortie
for out_dir in OUTPUT_DIRS:
    os.makedirs(out_dir, exist_ok=True)

# Fonction de luminosité
def brightness_score(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Image non lisible : {image_path}")
    return img.mean()

# Récupération des fichiers
filenames = [
    f for f in os.listdir(SOURCE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

# Traitement
for f in tqdm(filenames):
    path = os.path.join(SOURCE_DIR, f)
    try:
        score = brightness_score(path)

        if score <= THRESHOLDS[0]:
            dest_dir = OUTPUT_DIRS[0]
        elif score <= THRESHOLDS[1]:
            dest_dir = OUTPUT_DIRS[1]
        elif score <= THRESHOLDS[2]:
            dest_dir = OUTPUT_DIRS[2]
        else:
            dest_dir = OUTPUT_DIRS[3]

        shutil.copy2(path, os.path.join(dest_dir, f))
    except Exception as e:
        print(f"Erreur sur {f} : {e}")

print("✅ Tri par luminosité multiple terminé.")

scores = [brightness_score(os.path.join(SOURCE_DIR, f)) for f in filenames]
plt.hist(scores, bins=50)
plt.title("Distribution des luminosités moyennes")
plt.xlabel("Luminosité moyenne")
plt.ylabel("Nombre d'images")
for threshold in THRESHOLDS:
    plt.axvline(x=threshold, color="orange", linestyle="--", label=f"Seuil {threshold}")
plt.legend()
plt.show()
