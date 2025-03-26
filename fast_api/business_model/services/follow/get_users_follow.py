"""Данные пользователей, сведения о подписках"""
from typing import Type

from fastapi import status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User, UserFollower
from fast_api.factories import error_factory
from fast_api.logs import logger


async def get_users_and_subscription(
        own_user_id: int, target_user_id: int, db: AsyncSession
) -> tuple[Type[User] | None, Type[User] | None, UserFollower | None]:
    """Возвращает текущего пользователя,
     целевого пользователя и существующую подписку"""
    own_user = await db.get(User, own_user_id)
    target_user = await db.get(User, target_user_id)

    if not target_user:
        logger.error("Target user not found")
        await error_factory.handle_db_error(
            db=db,
            error=ValueError(),
            er_type="ValueError",
            message="Target user not found",
            st_code=status.HTTP_404_NOT_FOUND,
        )

    target_query = select(UserFollower).where(
        and_(
            UserFollower.subscribed_user_id == own_user.id,
            UserFollower.followed_user_id == target_user.id,
        )
    )
    existing_subscription = (
        await db.execute(target_query)
    ).scalars().one_or_none()

    return own_user, target_user, existing_subscription
