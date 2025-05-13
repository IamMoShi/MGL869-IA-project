from io import BytesIO

from PIL import Image


async def load_image(file):
    """

    Args:
        file: Path to the image file

    Returns: PIL Image

    """
    contents = await file.read()
    return Image.open(BytesIO(contents))
