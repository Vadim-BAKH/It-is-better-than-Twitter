"""Конфигурация моделей таблиц"""

import pytest
from fast_api.business_model.models import (Tweet, TweetLike, TweetMedia, User,
                                            UserFollower)
from sqlalchemy import ARRAY, Integer, String, UniqueConstraint
from sqlalchemy.orm import RelationshipProperty


@pytest.mark.config
def test_user_model_config():
    """Тест модели пользователя"""
    assert hasattr(User, "id")
    assert hasattr(User, "name")
    assert hasattr(User, "api_key")
    assert hasattr(User, "tweets")
    assert hasattr(User, "likes")
    assert hasattr(User, "followers")
    assert hasattr(User, "followed_users")
    assert isinstance(User.__table__.columns["id"].type, Integer)
    assert isinstance(User.__table__.columns["name"].type, String)
    assert isinstance(User.__table__.columns["api_key"].type, String)
    assert isinstance(User.tweets.property, RelationshipProperty)
    assert isinstance(User.likes.property, RelationshipProperty)
    assert isinstance(User.followers.property, RelationshipProperty)
    assert isinstance(User.followed_users.property, RelationshipProperty)

    assert User.__tablename__ == "user_account"
    for constraint in User.__table__.constraints:
        if isinstance(constraint, UniqueConstraint) and "api_key" in [
            col.name for col in constraint.columns
        ]:
            assert True
            return
    assert False, "UniqueConstraint для api_key не найден"


@pytest.mark.config
def test_tweet_config():
    """Тест модели твитов"""
    assert hasattr(Tweet, "id")
    assert hasattr(Tweet, "user_id")
    assert hasattr(Tweet, "tweet_data")
    assert hasattr(Tweet, "tweet_media_ids")
    assert hasattr(Tweet, "user")
    assert hasattr(Tweet, "likes")
    assert isinstance(Tweet.__table__.columns["id"].type, Integer)
    assert isinstance(Tweet.__table__.columns["user_id"].type, Integer)
    assert isinstance(Tweet.__table__.columns["tweet_data"].type, String)
    assert isinstance(Tweet.__table__.columns["tweet_media_ids"].type, ARRAY)
    assert isinstance(Tweet.user.property, RelationshipProperty)
    assert isinstance(Tweet.likes.property, RelationshipProperty)

    assert Tweet.__tablename__ == "tweets"


@pytest.mark.config
def test_like_config():
    """Тест модели лайков"""
    assert hasattr(TweetLike, "id")
    assert hasattr(TweetLike, "user_id")
    assert hasattr(TweetLike, "tweet_id")
    assert hasattr(TweetLike, "user")
    assert hasattr(TweetLike, "tweet")
    assert isinstance(TweetLike.__table__.columns["id"].type, Integer)
    assert isinstance(TweetLike.__table__.columns["user_id"].type, Integer)
    assert isinstance(TweetLike.__table__.columns["tweet_id"].type, Integer)
    assert isinstance(TweetLike.user.property, RelationshipProperty)
    assert isinstance(TweetLike.tweet.property, RelationshipProperty)

    assert TweetLike.__tablename__ == "like_tweet"
    for constraint in TweetLike.__table__.constraints:
        if (
            isinstance(constraint, UniqueConstraint)
            and "tweet_id" in [col.name for col in constraint.columns]
            and "user_id" in [col.name for col in constraint.columns]
        ):
            assert True
            return
    assert False, "UniqueConstraint для user_id and tweet_id не найден"


@pytest.mark.config
def test_follow_config():
    """Тест модели подписчиков"""
    assert hasattr(UserFollower, "id")
    assert hasattr(UserFollower, "subscribed_user_id")
    assert hasattr(UserFollower, "followed_user_id")
    assert isinstance(UserFollower.__table__.columns["id"].type, Integer)
    assert isinstance(
        UserFollower.__table__.columns["subscribed_user_id"].type, Integer
    )
    assert isinstance(
        UserFollower.__table__.columns["followed_user_id"].type, Integer
    )

    assert UserFollower.__tablename__ == "followers"
    for constraint in UserFollower.__table__.constraints:
        if (
            isinstance(constraint, UniqueConstraint)
            and "subscribed_user_id" in [
                col.name for col in constraint.columns
            ]
            and "followed_user_id" in [
                col.name for col in constraint.columns
            ]
        ):
            assert True
            return
    assert (
        False
    ), "UniqueConstraint для subscribed_user_id and followed_user_id не найден"


@pytest.mark.config
def test_media_config():
    """Тест модели медиа"""
    assert hasattr(TweetMedia, "id")
    assert hasattr(TweetMedia, "media_url")
    assert isinstance(TweetMedia.__table__.columns["id"].type, Integer)
    assert isinstance(TweetMedia.__table__.columns["media_url"].type, String)

    assert TweetMedia.__tablename__ == "tweet_media"
