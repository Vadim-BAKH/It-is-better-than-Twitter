"""Валидация и сериализация модели пользователя"""

from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    """Модель для сериализации
    и валидации пользователя"""

    name: str


class UserIn(BaseUser):
    """Модель для создания"""


class UserOut(BaseUser):
    """Модель для вывода информации"""

    api_key: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Модель списка пользователей"""

    users: list[UserOut]

    model_config = ConfigDict(from_attributes=True)
