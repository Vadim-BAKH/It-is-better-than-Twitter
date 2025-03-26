"""Сериализация ленты твитов"""

from typing import List

from pydantic import BaseModel


class Author(BaseModel):
    """Представляет автора твита"""

    id: int
    name: str


class TweetLike(BaseModel):
    """Представляет лайк"""

    user_id: int
    name: str


class Tweet(BaseModel):
    """Представляет твит"""

    id: int
    content: str
    attachments: List[str]  # Список ссылок
    author: Author
    likes: List[TweetLike]  # Список лайков


class UserFeedResponse(BaseModel):
    """Представляет ответ на запрос ленты"""

    result: bool
    tweets: List[Tweet]
