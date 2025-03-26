"""Лайки иных пользователей"""

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import TweetLike
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.user.get_user_id import \
    get_user_id_by_api_key
from fast_api.logs import logger
from fast_api.schemas import doing_schema


@handle_db_exceptions
async def like_fiction(
    tweet_id: int, api_key: str, db: AsyncSession
) -> doing_schema.DoingResult:
    """Переключает лайки и возвращает True"""

    own_id = await get_user_id_by_api_key(api_key=api_key, db=db)
    new_like = TweetLike(user_id=own_id, tweet_id=tweet_id)
    db.add(new_like)
    logger.info(f"Have adding like with tweet ID {tweet_id}")
    await db.commit()
    return doing_schema.DoingResult(result=True)
