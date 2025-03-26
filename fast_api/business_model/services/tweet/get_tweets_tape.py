"""Лента твитов"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from fast_api.business_model.models import Tweet, TweetLike, TweetMedia
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.schemas import tape_schema


@handle_db_exceptions
async def see_tweet_tape(db: AsyncSession) -> tape_schema.UserFeedResponse:
    """Получает ленту твитов, отсортированных по количеству лайков"""

    # Подзапрос для подсчета количества лайков
    # pylint: disable=E1102
    subquery_likes = select(
        TweetLike.tweet_id, func.count(TweetLike.id).label("like_count")
    ).group_by(TweetLike.tweet_id).subquery()

    # Основной запрос для получения твитов
    query_tweet_info = (
        select(Tweet)
        .options(
            joinedload(Tweet.user),
            selectinload(Tweet.likes),
        )
        .order_by(
            func.coalesce(
                select(subquery_likes.c.like_count)
                .where(subquery_likes.c.tweet_id == Tweet.id)
                .scalar_subquery(),
                0,
            ).desc()
        )
        .limit(15)
    )

    tweet_list = []
    result = await db.execute(query_tweet_info)
    tweets = result.scalars().all()

    # Формируем список твитов с информацией о лайках и медиа ссылках
    for tweet in tweets:
        like_list = [
            tape_schema.TweetLike(user_id=like.user.id, name=like.user.name)
            for like in tweet.likes
        ]

        attachments_list = [
            (await db.get(TweetMedia, mid)).media_url
            for mid in tweet.tweet_media_ids
            if tweet.tweet_media_ids
        ]
        tweet_list.append(
            tape_schema.Tweet(
                id=tweet.id,
                content=tweet.tweet_data,
                attachments=attachments_list,
                author=tape_schema.Author(
                    id=tweet.user_id,
                    name=tweet.user.name),
                likes=like_list,
            )
        )

    return tape_schema.UserFeedResponse(result=True, tweets=tweet_list)
