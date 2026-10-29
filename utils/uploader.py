import uuid
from pathlib import Path

import cloudinary
import cloudinary.uploader

from core.env import envConfig as settings
from utils.log import Log

logger = Log(__name__)

UPLOAD_FOLDER = "members"

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_image_to_storage_bucket_and_produce_url(file):
    try:
        # Unique id so two uploads named e.g. "photo.jpg" don't overwrite each other
        public_id = f"{Path(file['filename']).stem}-{uuid.uuid4().hex[:8]}"
        result = cloudinary.uploader.upload(
            file["content"],
            folder=UPLOAD_FOLDER,
            public_id=public_id,
            resource_type="image",
        )
        return result["secure_url"]
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
    return None


def _public_id_from_url(url: str) -> str:
    # https://res.cloudinary.com/<cloud>/image/upload/v123/members/name.jpg -> members/name
    path = url.split("/upload/")[-1]
    parts = path.split("/")
    if parts[0].startswith("v") and parts[0][1:].isdigit():
        parts = parts[1:]
    return str(Path("/".join(parts)).with_suffix(""))


def delete_image_from_storage_bucket(image_urls: list):
    try:
        for image in image_urls:
            public_id = _public_id_from_url(image)
            cloudinary.uploader.destroy(public_id, resource_type="image")
            logger.info(f"Image deleted: {public_id}")
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
        return False
    return True
