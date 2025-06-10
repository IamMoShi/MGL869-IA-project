from PIL import Image
from PIL.ExifTags import TAGS

def show_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if not exif_data:
        print("Aucune donnée EXIF trouvée.")
        return

    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        print(f"{tag_name:25}: {value}")

# Exemple d'utilisation
show_exif("images_raw/buildings-20057.jpg")
