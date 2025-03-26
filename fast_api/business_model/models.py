"""Конфигурация моделей"""

import os.path

import aiofiles
from fastapi import UploadFile, status
from sqlalchemy import (ARRAY, ForeignKey, Integer, Sequence, String,
                        UniqueConstraint, select)
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.tweet.process_tweet import \
    tweet_process_creation
from fast_api.factories import error_factory
from fast_api.factories.api_key_factory import create_unique_api_key
from fast_api.factories.media_name_factory import MEDIA_DIR, media_name
from fast_api.logs import logger
from fast_api.schemas import (doing_schema, followers_schema, media_schema,
                              tweet_schema, user_schema)
from fast_api.secret_mission.conf_env import MAIN_USER

Base = declarative_base()


class TweetLike(Base):
    """Модель лайков"""

    __tablename__ = "like_tweet"
    __table_args__ = (
        UniqueConstraint("user_id", "tweet_id", name="unique_like"),
    )
    id: Mapped[int] = mapped_column(Sequence(name="like_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="likes")
    tweet: Mapped["Tweet"] = relationship(back_populates="likes")

    def __repr__(self) -> str:
        """Возвращает строковое представление"""
        return (
            f"user's likes: "
            f"ID number {self.id!r}, "
            f"ID user {self.user_id!r}, "
            f"ID tweet {self.tweet_id!r}."
        )

    @classmethod
    @handle_db_exceptions
    async def like_toggle(
        cls, tweet_id: int, db: AsyncSession
    ) -> doing_schema.DoingResult:
        """Переключает лайки и возвращает True"""

        new_like = cls(user_id=MAIN_USER, tweet_id=tweet_id)
        db.add(new_like)
        await db.commit()
        logger.info(f"Have adding like with tweet ID {tweet_id}")
        return doing_schema.DoingResult(result=True)


class User(Base):
    """Модель пользователя"""

    __tablename__ = "user_account"
    __table_args__ = (UniqueConstraint("api_key", name="unique_api"),)

    id: Mapped[int] = mapped_column(Sequence("user_id"), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    api_key: Mapped[str] = mapped_column(String(50), nullable=False)

    tweets: Mapped[list["Tweet"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="select"
    )

    likes: Mapped[list["TweetLike"]] = relationship(back_populates="user")

    followers: Mapped[list["User"]] = relationship(
        secondary="followers",
        primaryjoin="User.id == UserFollower.followed_user_id",
        secondaryjoin="User.id == UserFollower.subscribed_user_id",
        back_populates="followed_users",
        lazy="select",
    )
    followed_users: Mapped[list["User"]] = relationship(
        secondary="followers",
        primaryjoin="User.id == UserFollower.subscribed_user_id",
        secondaryjoin="User.id == UserFollower.followed_user_id",
        back_populates="followers",
        lazy="select",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление"""
        return f"user's name: {self.name!r}, " f"api_key: {self.api_key!r}"

    @classmethod
    @handle_db_exceptions
    async def add_user(
        cls, user_in: user_schema.UserIn, db: AsyncSession
    ) -> user_schema.UserOut:
        """Добавляет пользователя"""

        api_key = create_unique_api_key(name=user_in.name)
        new_user = cls(name=user_in.name, api_key=api_key)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"user {new_user.id} created successfully")
        return user_schema.UserOut.model_validate(new_user)


class Tweet(Base):
    """Модель твитов"""

    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(Sequence("tweet_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    tweet_data: Mapped[str] = mapped_column(String(500), nullable=True)
    tweet_media_ids: Mapped[list[int] | None] = mapped_column(
        ARRAY(Integer), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="tweets")
    likes: Mapped[list["TweetLike"]] = relationship(
        back_populates="tweet", cascade="all, delete-orphan", lazy="joined"
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление"""
        return (
            f"user's tweet: user_id ({self.user_id!r}), "
            f"tweet_data ({self.tweet_data!r}), "
            f"tweet_media_ids ({self.tweet_media_ids!r})"
        )

    @classmethod
    @handle_db_exceptions
    async def create_tweet(
        cls, tweet_data: str, tweet_media_ids: list[int], db: AsyncSession
    ) -> tweet_schema.TweetOut:
        """Создает твит, возвращает его ID"""

        await tweet_process_creation(tweet_data=tweet_data, db=db)
        if tweet_media_ids is None or len(tweet_media_ids) == 0:
            new_tweet = Tweet(
                user_id=MAIN_USER,
                tweet_data=tweet_data,
                tweet_media_ids=[],
            )
        else:

            new_tweet = Tweet(
                user_id=MAIN_USER,
                tweet_data=tweet_data,
                tweet_media_ids=tweet_media_ids,
            )
        db.add(new_tweet)
        await db.commit()
        await db.refresh(new_tweet)
        logger.info(f"tweet {new_tweet.id} created successfully")

        return tweet_schema.TweetOut(result=True, tweet_id=new_tweet.id)


class UserFollower(Base):
    """Модель подписчиков"""

    __tablename__ = "followers"
    __table_args__ = (
        UniqueConstraint(
            "subscribed_user_id", "followed_user_id", name="unique_follower"
        ),
    )

    id: Mapped[int] = mapped_column(
        Sequence(name="followers_id"), primary_key=True
    )
    subscribed_user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False
    )
    followed_user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление"""
        return (
            f"Data follower: "
            f"ID number {self.id}; "
            f"subscribed ID {self.subscribed_user_id!r}; "
            f"followed ID {self.followed_user_id!r}."
        )

    @classmethod
    async def get_followers_table(cls, db: AsyncSession) -> dict:
        """Возвращает сведения таблицы"""
        query_follow = select(cls)
        follows = (await db.execute(query_follow)).scalars().all()
        return followers_schema.Follower.model_dump(**follows.__dict__)


class TweetMedia(Base):
    """Модель медиафайлов"""

    __tablename__ = "tweet_media"

    id: Mapped[int] = mapped_column(
        Sequence(name="tweet_media_id"), primary_key=True
    )

    media_url: Mapped[str] = mapped_column(String, nullable=False)

    #

    def __repr__(self) -> str:
        """Возвращает строковое представление"""
        return (
            f"Media data: " f"ID number {self.id!r};"
            f" " f"media URL {self.media_url!r}."
        )

    @classmethod
    @handle_db_exceptions
    async def upload_media(
        cls,
        media_file: UploadFile,
        db: AsyncSession,
    ) -> media_schema.MediaOut:
        """Загружает медиафайл и создает запись в базе данных"""

        if not media_file.filename.endswith((".jpg", ".jpeg")):
            await error_factory.handle_db_error(
                db=db,
                error=InvalidRequestError(),
                er_type="InvalidRequestError",
                message="Only .jpg files are allowed",
                st_code=status.HTTP_400_BAD_REQUEST,
            )
        new_name = media_name(file_name=media_file.filename)
        logger.info(f"New file name: {new_name}")
        file_path = os.path.join(MEDIA_DIR, new_name)
        logger.info(f"Path: {file_path}")
        content: bytes = await media_file.read()
        async with aiofiles.open(file_path, mode="wb") as image:
            await image.write(content)

        new_media = cls(media_url=new_name)
        db.add(new_media)
        await db.commit()
        await db.refresh(new_media)
        logger.info(f"Media with ID {new_media.id} received")

        return media_schema.MediaOut(result=True, media_id=new_media.id)
