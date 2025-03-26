"""Проверка существования пользователя"""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User
from fast_api.business_model.services.follow.follower_list import \
    get_follower_list
from fast_api.business_model.services.follow.following_list import \
    get_following_list
from fast_api.factories import error_factory
from fast_api.logs import logger
from fast_api.schemas.profile_schema import Follower, Following


async def check_user_by_user_id(
        user_id: int, db: AsyncSession
) -> tuple[Type[User] | None, list[Follower], list[Following]]:
    """Проверяет существование пользователя по ID"""

    user = await db.get(User, user_id)
    if not user:
        await error_factory.handle_db_error(
            db=db,
            error=ValueError(f"User with ID {user_id} not found"),
            er_type="NotFoundUserID",
            message="Not found user's ID",
            st_code=404,
        )
    logger.info(f"Have found user with ID {user_id}")
    followers_list = await get_follower_list(user_id=user.id, db=db)
    followings_list = await get_following_list(user_id=user.id, db=db)
    return user, followers_list, followings_list
