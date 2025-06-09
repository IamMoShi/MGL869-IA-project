import logging
from typing import Sequence

from app.core.database import get_db
from app.models.image import Image
from app.services.database import (
    get_all_images,
    get_images_since,
    get_latest_images,
    get_random_images,
)
from app.services.images.augmentation import augment_images_from_minio
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("uvicorn")
router = APIRouter()


@router.get("/process", tags=["process"])
async def process(db: AsyncSession = Depends(get_db)):
    # last_images: Sequence[Image] = await get_latest_images(db, limit=1000)
    # random_images: Sequence[Image] = await get_random_images(db, limit=500)

    # Merge the two sequences without duplicates, using set with the IDs
    # image_dict = {image.id: image for image in last_images}
    # image_dict.update({image.id: image for image in random_images})
    # unique_images = list(image_dict.values())

    unique_images = await get_all_images(db)

    # Prepare data for the increase
    images_data = [(image.filename, image.category) for image in unique_images]
    augment_images_from_minio(images_data, naming="all_images")

    return unique_images
