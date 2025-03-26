"""Схема профиля пользователя"""

from pydantic import BaseModel, ConfigDict


class Me(BaseModel):
    """Ввод Api-key"""

    api_key: str


class Follower(BaseModel):
    """Подписчики"""

    id: int
    name: str


class Following(BaseModel):
    """Подписки"""

    id: int
    name: str


class User(BaseModel):
    """Схема пользователя"""

    id: int
    name: str
    followers: list[Follower]
    following: list[Following]

    model_config = ConfigDict(from_attributes=True)


class ProfileBase(BaseModel):
    """Информация о профиле"""

    result: bool
    user: User

    model_config = ConfigDict(from_attributes=True)
