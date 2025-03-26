"""Создание стороннего твита"""

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import Tweet
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.tweet.process_tweet import \
    tweet_process_creation
from fast_api.business_model.services.user.get_user_id import \
    get_user_id_by_api_key
from fast_api.logs import logger
from fast_api.schemas import tweet_schema


@handle_db_exceptions
async def create_tweet_fiction(
    api_key: str,
    tweet_data: str,
    tweet_media_ids: list[int],
    db: AsyncSession
) -> tweet_schema.TweetOut:
    """Создает твит, возвращает его ID"""
    await tweet_process_creation(tweet_data=tweet_data, db=db)
    user_id = await get_user_id_by_api_key(api_key=api_key, db=db)
    if tweet_media_ids is None or len(tweet_media_ids) == 0:

        tweet = Tweet(
            user_id=user_id,
            tweet_data=tweet_data,
            tweet_media_ids=[],
        )
    else:

        tweet = Tweet(
            user_id=user_id,
            tweet_data=tweet_data,
            tweet_media_ids=tweet_media_ids,
        )
    db.add(tweet)
    await db.commit()
    await db.refresh(tweet)
    logger.info(f"tweet {tweet.id} created successfully")

    return tweet_schema.TweetOut(result=True, tweet_id=tweet.id)
