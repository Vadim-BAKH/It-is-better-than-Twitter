"""Список лиц, на которых подписан пользователь"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User, UserFollower
from fast_api.schemas.profile_schema import Following


async def get_following_list(
        user_id: int, db: AsyncSession
) -> list[Following]:
    """Возвращает всех на кого подписан пользователь по ID"""
    # Запрос подписок (на кого подписан пользователь)
    followings_query = (
        select(User)
        .join(UserFollower, User.id == UserFollower.followed_user_id)
        .where(UserFollower.subscribed_user_id == user_id)
    )
    followings = (await db.execute(followings_query)).scalars().all()
    followings_list = [
        Following(
            id=following.id, name=following.name
        ) for following in followings
    ]
    return followings_list
