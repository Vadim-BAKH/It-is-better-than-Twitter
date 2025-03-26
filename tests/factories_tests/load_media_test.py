"""Тестовая загрузка медиа"""

import os
from io import BytesIO


async def load_media():
    """Создаёт форму с файлом"""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(current_dir, "media_testing/")

    media_path = os.path.join(media_dir, "птичка.jpg")

    with open(media_path, "rb") as file:
        file_content = file.read()

    return {
        "file": (
            "птичка.jpg",
            BytesIO(file_content),
            "image/jpeg",
        )
    }
