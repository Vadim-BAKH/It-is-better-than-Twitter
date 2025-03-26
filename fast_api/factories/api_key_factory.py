"""Фабрика уникального api-key"""

import uuid
from hashlib import sha256


def create_unique_api_key(name: str) -> str:
    """Возвращает уникальный api_key"""
    unique_key = sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest()[:8]
    return f"{name}@{unique_key}"
