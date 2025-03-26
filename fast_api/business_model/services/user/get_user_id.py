"""Получение ID пользователя"""
from typing import Optional

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User
from fast_api.factories import error_factory
from fast_api.logs import logger


async def get_user_id_by_api_key(
        api_key: str, db: AsyncSession
) -> Optional[int]:
    """Возвращает ID пользователя по api_key"""

    query = select(User.id).where(User.api_key == api_key)
    response = await db.execute(query)
    user_id: int | None = response.scalars().one_or_none()
    if user_id is None:
        await error_factory.handle_db_error(
            db=db,
            error=ValueError(f"User with api_key {api_key} not found"),
            er_type="NotFoundApiKey",
            message="Not found Api-key",
            st_code=status.HTTP_401_UNAUTHORIZED,
        )
    logger.info(f"Have found user with api-key {api_key}")
    return user_id
