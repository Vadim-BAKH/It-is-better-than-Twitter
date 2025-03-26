"""Длина строки твита"""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.factories import error_factory


async def tweet_process_creation(
    tweet_data: str, db: AsyncSession
) -> bool | None:
    """Возвращает True по длине строки"""

    if len(tweet_data) > 500:
        await error_factory.handle_db_error(
            db=db,
            error=ValueError(),
            er_type="ExcLimitCharacters",
            message="tweet exceeds 500 characters limit",
            st_code=status.HTTP_400_BAD_REQUEST,
        )

    return True
