"""Список подписчиков на пользователя"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User, UserFollower
from fast_api.schemas.profile_schema import Follower


async def get_follower_list(user_id: int, db: AsyncSession) -> list[Follower]:
    """Возвращает всех кто подписан на пользователя ID"""
    # Запрос подписчиков (кто подписан на пользователя)
    followers_query = (
        select(User)
        .join(UserFollower, User.id == UserFollower.subscribed_user_id)
        .where(UserFollower.followed_user_id == user_id)
    )
    followers = (await db.execute(followers_query)).scalars().all()

    followers_list = [
        Follower(id=follower.id, name=follower.name) for follower in followers
    ]

    return followers_list
