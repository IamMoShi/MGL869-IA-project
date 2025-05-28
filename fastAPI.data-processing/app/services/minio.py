import io
import logging
from typing import Union

from app.core.minio import s3_client
from PIL import Image as PILImage

logger = logging.getLogger("uvicorn")


def get_image_from_minio(key: str, bucket: str) -> Union[PILImage, None]:
    """Download an image from MinIO and convert it to a PIL Image.

    :param key: The key of the image in the bucket.
    :param bucket: The name of the bucket where the image is stored.
    :return: A PIL Image object if successful, None otherwise.
    """
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        img: PILImage = PILImage.open(io.BytesIO(obj["Body"].read())).convert(
            "RGB"
        )
        return img
    except Exception as e:
        logger.error(f"Failed to load {key}: {str(e).replace('\n', '\\n')}")
        return None


def save_image_to_minio(
    image: PILImage.Image, key: str, bucket: str, img_format: str = "JPEG"
) -> None:
    """Save a PIL Image to MinIO.

    :param image: The PIL Image to save.
    :param bucket: The name of the bucket where the image will be saved.
    :param key: The key under which to save the image in the bucket.
    :param img_format: The format to save the image in (default is
        "JPEG").
    :return: None
    """
    buffer = io.BytesIO()
    image.save(buffer, format=img_format)
    buffer.seek(0)

    s3_client.upload_fileobj(
        Fileobj=buffer,
        Bucket=bucket,
        Key=key,
        ExtraArgs={"ContentType": f"image/{img_format.lower()}"},
    )
