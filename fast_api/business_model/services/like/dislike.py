"""Удаление записи о лайке"""

from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import TweetLike
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.logs import logger
from fast_api.schemas import doing_schema
from fast_api.secret_mission.conf_env import MAIN_USER


@handle_db_exceptions
async def dislike_toggle(
        tweet_id: int,
        db: AsyncSession
) -> doing_schema.DoingResult:
    """Переключает лайки и возвращает True"""

    own_id = MAIN_USER
    tweet_like_query = delete(TweetLike).where(
        and_(TweetLike.tweet_id == tweet_id, TweetLike.user_id == own_id)
    )
    await db.execute(tweet_like_query)

    logger.info(f"Have delete like with tweet ID {tweet_id}")
    await db.commit()
    return doing_schema.DoingResult(result=True)
