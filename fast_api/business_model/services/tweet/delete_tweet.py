"""Удаление твита"""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import Tweet
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.factories import error_factory
from fast_api.logs import logger
from fast_api.schemas import doing_schema
from fast_api.secret_mission.conf_env import MAIN_USER


@handle_db_exceptions
async def kill_tweet(
        tweet_id: int,
        db: AsyncSession
) -> doing_schema.DoingResult:
    """Удаляет свой твит, возвращает True"""

    own_id = MAIN_USER
    tweet = await db.get(Tweet, tweet_id)
    if not tweet or tweet.user_id != own_id:
        await error_factory.handle_db_error(
            db=db,
            error=ValueError("An attempt to remove someone else's tweet"),
            er_type="ValueError",
            message="An attempt to remove someone else's tweet",
            st_code=status.HTTP_404_NOT_FOUND,
        )
    await db.delete(tweet)
    await db.commit()

    logger.info(f"Have delete tweet with tweet ID {tweet_id}")

    return doing_schema.DoingResult(result=True)
