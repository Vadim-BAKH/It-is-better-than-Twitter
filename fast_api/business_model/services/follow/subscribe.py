"""Подписка на пользователя"""

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import UserFollower
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.follow.get_users_follow import \
    get_users_and_subscription
from fast_api.logs import logger
from fast_api.schemas import doing_schema
from fast_api.schemas.doing_schema import DoingResult
from fast_api.secret_mission.conf_env import MAIN_USER


@handle_db_exceptions
async def subscribe_to(
    target_user_id: int, db: AsyncSession
) -> DoingResult | None:
    """Подписывает на пользователя, возвращает True"""

    own_user, target_user, existing_subscription = \
        await get_users_and_subscription(
            own_user_id=MAIN_USER, target_user_id=target_user_id, db=db
        )
    if not existing_subscription:
        new_subscription = UserFollower(
            subscribed_user_id=own_user.id,
            followed_user_id=target_user.id
        )
        db.add(new_subscription)
        logger.info(f"Have subscribing to user_id: {target_user.id}")
        await db.commit()

        return doing_schema.DoingResult(result=True)

    return None
