from pydantic import BaseModel


class ImageMetadata(BaseModel):
    """Specify structure of image metadata."""

    filename: str
    content_type: str
