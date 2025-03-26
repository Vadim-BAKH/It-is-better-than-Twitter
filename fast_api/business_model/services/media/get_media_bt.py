"""Отображения медиафайла"""

import os

from fastapi import status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import TweetMedia
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.factories import error_factory
from fast_api.factories.media_name_factory import MEDIA_DIR
from fast_api.logs import logger


@handle_db_exceptions
async def see_media_by_id(media_id: int, db: AsyncSession) -> FileResponse:
    """Открывает медиафайл по ссылке"""

    media = await db.get(TweetMedia, media_id)
    if not media:
        logger.error(f"media ID {media_id} Not Found")
        await error_factory.handle_db_error(
            db=db,
            error=ValueError(),
            er_type="ValueError",
            message="media ID Not Found",
            st_code=status.HTTP_404_NOT_FOUND,
        )
    file_path = str(os.path.join(MEDIA_DIR, media.media_url))
    if not os.path.exists(file_path):
        logger.error(f"media file {file_path} Not Found")
        await error_factory.handle_db_error(
            db=db,
            error=FileNotFoundError(),
            er_type="FileNotFoundError",
            message="media file Not Found",
            st_code=status.HTTP_404_NOT_FOUND,
        )
    return FileResponse(path=file_path, filename=media.media_url)
