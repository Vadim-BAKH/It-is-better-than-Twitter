"""Ссылка на медиафайл"""

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import TweetMedia
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.schemas.media_schema import MediaLink


@handle_db_exceptions
async def media_link(
        media_id: int, db: AsyncSession
) -> MediaLink:
    """Возвращает ссылку на медиа файл по ID"""
    media = await db.get(TweetMedia, media_id)
    return MediaLink(media_url=media.media_url)
