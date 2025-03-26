"""Создание медиафайла"""

import uuid
from hashlib import sha256
from pathlib import Path

MEDIA_DIR = Path("/usr/share/nginx/html/static/media")


def media_name(file_name: str) -> str:
    """Создает уникальное имя файла"""

    unique_code = sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()[:6]
    return f"{unique_code}_{file_name}"
