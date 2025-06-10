import os
import shutil
import torch
import clip
from PIL import Image
from sklearn.cluster import KMeans
from tqdm import tqdm

# --- CONFIG ---
SRC_DIR = "seg_test"       # dossier source avec sous-dossiers catégorie
RAW_DIR = "images_raw"     # dossier cible des images renommées
CLUSTERS_DIR = "clusters"  # dossier des clusters
N_CLUSTERS = 6             # nombre de clusters à créer

# --- Création dossier images_raw ---
os.makedirs(RAW_DIR, exist_ok=True)

# --- Copie + renommage ---
print("📁 Copie et renommage des images...")
for category in os.listdir(SRC_DIR):
    category_path = os.path.join(SRC_DIR, category)
    if not os.path.isdir(category_path):
        continue

    for filename in os.listdir(category_path):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        src_file = os.path.join(category_path, filename)
        # Nouveau nom : "category-nom.jpg"
        new_name = f"{category}-{filename}"
        dst_file = os.path.join(RAW_DIR, new_name)
        shutil.copy2(src_file, dst_file)

print(f"✅ {len(os.listdir(RAW_DIR))} images copiées et renommées dans '{RAW_DIR}'")

# --- Chargement modèle CLIP ---
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# --- Extraction embeddings ---
print("🔍 Extraction des vecteurs visuels CLIP...")
image_paths = [
    os.path.join(RAW_DIR, f)
    for f in os.listdir(RAW_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

features = []
valid_paths = []

for path in tqdm(image_paths):
    try:
        image = preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            feature = model.encode_image(image)
            features.append(feature.cpu().numpy().flatten())
            valid_paths.append(path)
    except Exception as e:
        print(f"Erreur avec {path}: {e}")

# --- Clustering ---
print(f"📊 Clustering KMeans en {N_CLUSTERS} clusters...")
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42)
labels = kmeans.fit_predict(features)

# --- Création dossiers clusters + copie ---
print("📂 Répartition des images dans les clusters...")
for idx, label in enumerate(labels):
    cluster_folder = os.path.join(CLUSTERS_DIR, f"cluster_{label}")
    os.makedirs(cluster_folder, exist_ok=True)
    shutil.copy2(valid_paths[idx], os.path.join(cluster_folder, os.path.basename(valid_paths[idx])))

print("✅ Clustering terminé.")
