import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm

# === CONFIGURATION ===
INPUT_FOLDER = "images_raw"
OUTPUT_FOLDER = "images_split"
CRITERION = "DateTime"  # Peut être "Model", "Make", "Orientation", "DateTime", etc.

# === FONCTIONS ===
def extract_exif(img_path):
    try:
        img = Image.open(img_path)
        exif_data = img._getexif()
        if not exif_data:
            return {}
        return {
            TAGS.get(tag): value
            for tag, value in exif_data.items()
            if tag in TAGS
        }
    except Exception as e:
        print(f"[Warning] Could not read EXIF from {img_path}: {e}")
        return {}

def categorize_by_criterion(exif_data, criterion):
    value = exif_data.get(criterion, "Unknown")
    if isinstance(value, str):
        return value.replace(":", "-").replace(" ", "_")[:30]
    return str(value)

def process_images(input_folder, output_folder, criterion):
    os.makedirs(output_folder, exist_ok=True)
    images = [f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    for img_file in tqdm(images, desc="Processing images"):
        img_path = os.path.join(input_folder, img_file)
        exif = extract_exif(img_path)
        category = categorize_by_criterion(exif, criterion)

        category_folder = os.path.join(output_folder, category)
        os.makedirs(category_folder, exist_ok=True)

        shutil.copy2(img_path, os.path.join(category_folder, img_file))

# === LANCEMENT ===
if __name__ == "__main__":
    print(f"Tri des images par métadonnée : {CRITERION}")
    process_images(INPUT_FOLDER, OUTPUT_FOLDER, CRITERION)
    print("✅ Tri terminé.")
