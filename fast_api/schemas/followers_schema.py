"""Валидация и сериализация модели подписчика"""

from pydantic import BaseModel, ConfigDict


class BaseFollower(BaseModel):
    """Модель для сериализации
    и валидации подписчиков"""

    api_key: str
    followed_user_id: int


class FollowerIn(BaseFollower):
    """Модель для создания"""


class Follower(BaseModel):
    """Модель для вывода информации"""

    id: int
    subscribed_user_id: int
    followed_user_id: int

    model_config = ConfigDict(from_attributes=True)
