import uuid
from pathlib import Path

import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status

from app.core import cloudinary as cloudinary_config
from app.core.upload_config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_TYPES,
    MAX_IMAGE_SIZE,
)


async def save_tank_image(
    file: UploadFile,
) -> tuple[str, str]:
    """
    Validate and upload a tank image to Cloudinary.

    Returns:
        tuple[str, str]:
            - secure Cloudinary image URL
            - Cloudinary public ID
    """

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image file is required.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image extension. Allowed: JPG, JPEG, PNG, WEBP.",
        )

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image type. Allowed: JPEG, PNG, WEBP.",
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty.",
        )

    if len(file_content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image file is too large. Maximum size is 5 MB.",
        )

    public_id = f"kentank/tanks/{uuid.uuid4().hex}"

    try:
        upload_result = cloudinary.uploader.upload(
            file_content,
            public_id=public_id,
            resource_type="image",
            overwrite=False,
            secure=True,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to upload image to Cloudinary.",
        )

    secure_url = upload_result.get("secure_url")
    returned_public_id = upload_result.get("public_id")

    if not secure_url or not returned_public_id:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Cloudinary returned an invalid upload response.",
        )

    return secure_url, returned_public_id