"""Страница владельца профиля"""

from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.services.decorator.error_decorator import \
    handle_db_exceptions
from fast_api.business_model.services.user.check_user import \
    check_user_by_user_id
from fast_api.schemas import profile_schema
from fast_api.secret_mission.conf_env import MAIN_USER


@handle_db_exceptions
async def get_my_profile(db: AsyncSession) -> profile_schema.ProfileBase:
    """Возвращает профиль пользователя приложения"""

    user, followers_list, followings_list =\
        await check_user_by_user_id(user_id=MAIN_USER, db=db)

    me_profile = profile_schema.User(
        id=user.id,
        name=user.name,
        followers=followers_list,
        following=followings_list,
    )
    profile_result = profile_schema.ProfileBase(result=True, user=me_profile)
    return profile_result
