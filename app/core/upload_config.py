from pathlib import Path


# Base upload directory
UPLOAD_DIR = Path("uploads/tanks")


# Maximum image size: 5 MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024


# Allowed image MIME types
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def ensure_upload_directory() -> None:
    """
    Create the tank image upload directory if it does not exist.
    """
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )