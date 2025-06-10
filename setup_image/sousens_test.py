import os
import requests
from sklearn.metrics import classification_report
from collections import defaultdict

# --- Configuration ---
CLUSTERS_DIR = "brightness"
ANALYZE_API_URL = "http://127.0.0.1:5000/api/v1/analyze/predict"

true_labels = []
pred_labels = []
cluster_scores = defaultdict(lambda: {"y_true": [], "y_pred": []})

# --- Analyse des clusters ---
for cluster_name in os.listdir(CLUSTERS_DIR):
    cluster_path = os.path.join(CLUSTERS_DIR, cluster_name)
    if not os.path.isdir(cluster_path):
        continue

    for filename in os.listdir(cluster_path):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # 💡 Vraie étiquette depuis le nom du fichier : "forest_001.jpg"
        true_label = filename.split("-")[0].lower()

        try:
            with open(os.path.join(cluster_path, filename), "rb") as img_file:
                resp = requests.post(
                    ANALYZE_API_URL,
                    files={"file": (filename, img_file, "image/jpeg")},
                )
                resp.raise_for_status()
                pred_label = resp.json()["prediction"]
            # Global stats
            true_labels.append(true_label)
            pred_labels.append(pred_label)

            # Cluster-specific
            cluster_scores[cluster_name]["y_true"].append(true_label)
            cluster_scores[cluster_name]["y_pred"].append(pred_label)

        except Exception as e:
            print(f"Erreur avec {filename} : {e}")

    print(f"Cluster '{cluster_name}' traité.")

# --- Rapport global ---
print("📊 Rapport global :")
print(classification_report(true_labels, pred_labels, digits=3))

# --- Rapports par cluster ---
print("\n📁 Rapports par cluster :")
for cluster_name, scores in cluster_scores.items():
    print(f"\n--- {cluster_name} ---")
    if scores["y_true"]:
        print(classification_report(scores["y_true"], scores["y_pred"], digits=3))
    else:
        print("Aucune image traitée.")
