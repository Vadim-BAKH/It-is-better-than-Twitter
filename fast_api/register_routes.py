"""Регистрация маршрутов Flask-приложения."""

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.business_model.models import Tweet, TweetLike, TweetMedia, User
from fast_api.business_model.services.follow import (other_subscribe,
                                                     subscribe, unsubscribe)
from fast_api.business_model.services.like import dislike, other_user_like
from fast_api.business_model.services.media import get_media_bt, get_media_link
from fast_api.business_model.services.tweet import (create_tweet_fiction,
                                                    delete_tweet,
                                                    get_tweets_tape)
from fast_api.business_model.services.user import (get_profile_myself,
                                                   get_somebody_profile,
                                                   see_all_users)
from fast_api.database import get_session_db
from fast_api.logs import logger
from fast_api.schemas import (doing_schema, media_schema, profile_schema,
                              tape_schema, tweet_schema, user_schema)

templates = Jinja2Templates(directory="fast_api/templates")

router = APIRouter(
    prefix="/api",
    tags=["twitter"],
)


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_class=HTMLResponse)
async def get_main_html(request: Request):
    """Возвращает html шаблон"""

    return templates.TemplateResponse(name="index.html", request=request)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.UserOut
)
async def create_new_user(
    user_in: user_schema.UserIn, db: AsyncSession = Depends(get_session_db)
) -> user_schema.UserOut:
    """Создает нового пользователя, возвращает
    его данные из таблицы"""

    return await User.add_user(user_in=user_in, db=db)


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.UserListResponse,
)
async def get_all_users(
    db: AsyncSession = Depends(get_session_db),
) -> user_schema.UserListResponse:
    """Возвращает всех пользователей"""
    return await see_all_users.all_users(db=db)


@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=profile_schema.ProfileBase,
)
async def see_my_profile(
    db: AsyncSession = Depends(get_session_db),
) -> profile_schema.ProfileBase:
    """Возвращает профиль главного пользователя
    странички"""

    return await get_profile_myself.get_my_profile(db=db)


@router.post(
    "/tweets",
    status_code=status.HTTP_201_CREATED,
    response_model=tweet_schema.TweetOut
)
async def tweet(
    tweet_in: tweet_schema.BaseTweet,
        db: AsyncSession = Depends(get_session_db)
) -> tweet_schema.TweetOut:
    """Создаёт твит, возвращает ID, True"""

    return await Tweet.create_tweet(
        tweet_data=tweet_in.tweet_data,
        tweet_media_ids=tweet_in.tweet_media_ids,
        db=db
    )


@router.get(
    "/tweets",
    status_code=status.HTTP_200_OK,
    response_model=tape_schema.UserFeedResponse,
)
async def get_tweets_all(
    db: AsyncSession = Depends(get_session_db),
) -> tape_schema.UserFeedResponse:
    """Возвращает ленту твитов."""
    return await get_tweets_tape.see_tweet_tape(db=db)


@router.post(
    "/medias",
    status_code=status.HTTP_201_CREATED,
    response_model=media_schema.MediaOut
)
async def load_media(
    request: Request,
    db: AsyncSession = Depends(get_session_db),
) -> media_schema.MediaOut:
    """Записывает медиа, создаёт ссылку, возвращает
    ID записи и True"""
    form = await request.form()
    logger.info(f"Form data: {form}")
    media_file = form.get("file")
    logger.info(f"file_name {media_file.filename}")
    return await TweetMedia.upload_media(media_file=media_file, db=db)


@router.get(
    "/users/{idu}",
    status_code=status.HTTP_200_OK,
    response_model=profile_schema.ProfileBase,
)
async def get_profile_somebody(
        idu: int, db: AsyncSession = Depends(get_session_db)
) -> profile_schema.ProfileBase:
    """Возвращает профиль пользователя"""
    return await get_somebody_profile.see_somebody_profile(
        user_id=idu, db=db
    )


@router.get(
    "/medias/{media_id}", response_class=FileResponse, status_code=200
)
async def get_media_by_id(
        media_id: int, db: AsyncSession = Depends(get_session_db)
):
    """Открывает ссылку на файл по ID"""
    return await get_media_bt.see_media_by_id(media_id=media_id, db=db)


@router.post(
    "/tweets/{idt}/like_fiction",
    status_code=status.HTTP_201_CREATED,
    response_model=doing_schema.DoingResult,
)
async def fiction_like(
    idt: int,
    api_key: doing_schema.OtherUser,
    db: AsyncSession = Depends(get_session_db),
) -> doing_schema.DoingResult:
    """Ставит лайк от другого пользователя,
    возвращает True"""
    return await other_user_like.like_fiction(
        tweet_id=idt, api_key=api_key.api_key, db=db
    )


@router.post(
    "/tweets/{idt}/likes",
    status_code=status.HTTP_201_CREATED,
    response_model=doing_schema.DoingResult,
)
async def like(
    idt: int,
    db: AsyncSession = Depends(get_session_db),
) -> doing_schema.DoingResult:
    """Ставит лайк, возвращает True"""
    return await TweetLike.like_toggle(tweet_id=idt, db=db)


@router.delete(
    "/tweets/{idt}/likes",
    status_code=status.HTTP_200_OK,
    response_model=doing_schema.DoingResult,
)
async def like_remove(
    idt: int,
    db: AsyncSession = Depends(get_session_db),
) -> doing_schema.DoingResult:
    """Удаляет лайк, возвращает True"""
    return await dislike.dislike_toggle(tweet_id=idt, db=db)


@router.delete(
    "/tweets/{idt}",
    status_code=status.HTTP_200_OK,
    response_model=doing_schema.DoingResult,
)
async def delete_own_tweet(
    idt: int, db: AsyncSession = Depends(get_session_db)
) -> doing_schema.DoingResult:
    """Удаляет собственный твит, возвращает True"""
    return await delete_tweet.kill_tweet(tweet_id=idt, db=db)


@router.post(
    "/users/{idu}/follow",
    status_code=status.HTTP_201_CREATED,
    response_model=doing_schema.DoingResult,
)
async def subscribe_to_user(
    idu: int, db: AsyncSession = Depends(get_session_db)
) -> doing_schema.DoingResult:
    """Подписывает на пользователя, возвращает True"""
    return await subscribe.subscribe_to(target_user_id=idu, db=db)


@router.delete(
    "/users/{idu}/follow",
    status_code=status.HTTP_200_OK,
    response_model=doing_schema.DoingResult,
)
async def unsubscribe_from_user(
    idu: int, db: AsyncSession = Depends(get_session_db)
) -> doing_schema.DoingResult:
    """Отписывает от пользователя, возвращает True"""
    return await unsubscribe.unsubscribe_from(target_user_id=idu, db=db)


@router.post(
    "/users/{idu}/follow_fiction",
    status_code=status.HTTP_201_CREATED,
    response_model=doing_schema.DoingResult,
)
async def fiction_subscribe_to_user(
    idu: int,
    api_key: doing_schema.OtherUser,
    db: AsyncSession = Depends(get_session_db),
) -> doing_schema.DoingResult:
    """Подписывает на пользователя, возвращает True"""
    return await other_subscribe.fiction_subscribe_to(
        target_user_id=idu, api_key=api_key.api_key, db=db
    )


@router.post(
    "/tweets_fiction",
    status_code=status.HTTP_201_CREATED,
    response_model=tweet_schema.TweetOut,
)
async def tweet_fiction(
    tweet_in: tweet_schema.TweetFiction,
    db: AsyncSession = Depends(get_session_db)
) -> tweet_schema.TweetOut:
    """Создаёт сторонний фиктивный твит"""

    return await create_tweet_fiction.create_tweet_fiction(
        api_key=tweet_in.api_key,
        tweet_data=tweet_in.tweet_data,
        tweet_media_ids=tweet_in.tweet_media_ids,
        db=db,
    )


@router.get(
    "/media_url/{idm}",
    status_code=status.HTTP_200_OK,
    response_model=media_schema.MediaLink
)
async def see_media_url(
        idm: int, db: AsyncSession = Depends(get_session_db)
) -> media_schema.MediaLink:
    """Возвращает ссылку на медиа файл по ID"""
    return await get_media_link.media_link(media_id=idm, db=db)
