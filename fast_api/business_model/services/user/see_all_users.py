"""Посмотреть всех пользователей"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import User
from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.schemas import user_schema


@handle_db_exceptions
async def all_users(db: AsyncSession) -> user_schema.UserListResponse:
    """Возвращает данные всех пользователей"""

    all_users_query = select(User)
    all_users_list = (await db.execute(all_users_query)).scalars().all()
    users = [user_schema.UserOut(**user.__dict__) for user in all_users_list]
    return user_schema.UserListResponse(users=users)
