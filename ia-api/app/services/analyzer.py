import io

import torch
from PIL import Image
from torchvision import transforms

from app.utils.image_tools import load_image
from fastapi import UploadFile

CLASSES = ["buildings", "forest", "glacier", "mountain", "sea", "street"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet standard
        std=[0.229, 0.224, 0.225]
    )
])

device = torch.device("cpu")
model = torch.jit.load("app/models/mobilenet_scripted.pt", map_location=device)
model.eval()

# Fictitious example with an IA model
async def predict_from_bytes(image_bytes: bytes):
    """

    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)
        predicted_idx = torch.argmax(output, dim=1).item()
    return CLASSES[predicted_idx]
