"""Валидация и сериализация модели лайк"""

from pydantic import BaseModel, ConfigDict


class OtherUser(BaseModel):
    """Модель для лайков других пользователей"""

    api_key: str


class DoingResult(BaseModel):
    """Модель для вывода информации"""

    result: bool

    model_config = ConfigDict(from_attributes=True)
