"""Валидация и сериализация модели твита"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseTweet(BaseModel):
    """Модель для сериализации
    и валидации твитов"""

    tweet_data: str
    tweet_media_ids: Optional[list[int]] = None


class TweetFiction(BaseTweet):
    """Модель для фиктивной сериализации
    и валидации твитов"""

    api_key: str
    tweet_data: str
    tweet_media_ids: Optional[list[int]] = None


#
# class TweetIn(BaseTweet):
#     """Модель для создания"""
#
#     @classmethod
#     @model_validator(mode="before")
#     def remove_zero_ids(cls, values):
#         """Удаляет 0 из списка"""
#         if values.get("tweet_media_ids"):
#             values["tweet_media_ids"] = [
#                 ids for ids in values["tweet_media_ids"] if ids != 0
#             ]
#             if not values["tweet_media_ids"]:
#                 values["tweet_media_ids"] = None
#         else:
#             values["tweet_media_ids"] = None
#         return values
#


class TweetOut(BaseModel):
    """Модель для вывода информации"""

    result: bool
    tweet_id: int

    model_config = ConfigDict(from_attributes=True)
