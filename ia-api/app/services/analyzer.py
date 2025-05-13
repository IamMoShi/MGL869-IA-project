from app.utils.image_tools import load_image
from fastapi import UploadFile


# Fictitious example with an IA model
async def analyze_image(file: UploadFile):
    """

    Args:
        file: TODO

    Returns: TODO

    """
    image = await load_image(file)
    print("Image format :", image.format)  # Modify to use IA model
    print("Image size   :", image.size)
    print("Image mode   :", image.mode)
    prediction = "detected_object"
    return prediction
