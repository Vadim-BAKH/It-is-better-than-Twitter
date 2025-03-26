"""Валидация и сериализация модели медиа"""

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class MediaLink(BaseModel):
    """Модель возвращает ссылку"""
    media_url: str


class MediaUpload(BaseModel):
    """Модель записи медиафайла"""
    tweet_id: int
    media_file: UploadFile


class MediaOut(BaseModel):
    """Модель для вывода информации"""

    result: bool
    media_id: int

    model_config = ConfigDict(from_attributes=True)
