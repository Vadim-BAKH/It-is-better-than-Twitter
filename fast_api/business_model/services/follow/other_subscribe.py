"""Подписка на пользователя"""


from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import UserFollower
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.follow.get_users_follow import \
    get_users_and_subscription
from fast_api.business_model.services.user.get_user_id import \
    get_user_id_by_api_key
from fast_api.logs import logger
from fast_api.schemas import doing_schema


@handle_db_exceptions
async def fiction_subscribe_to(
    target_user_id: int, api_key: str, db: AsyncSession
) -> doing_schema.DoingResult:
    """Подписывает на пользователя, возвращает True"""

    own_user_id = await get_user_id_by_api_key(api_key=api_key, db=db)
    own_user, target_user, existing_subscription = \
        await get_users_and_subscription(
            own_user_id=own_user_id, target_user_id=target_user_id, db=db
        )
    if not existing_subscription:
        subscription = UserFollower(
            subscribed_user_id=own_user.id,
            followed_user_id=target_user.id
        )
        db.add(subscription)
        logger.info(f"Have subscribing to user_id: {target_user.id}")
        await db.commit()
        return doing_schema.DoingResult(result=True)
