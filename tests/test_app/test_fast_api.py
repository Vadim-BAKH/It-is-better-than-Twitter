"""Цикл работы приложения"""

import pytest
from fast_api.logs import logger

from tests.test_app.chat_process import (create_media, create_user,
                                         delete_follow, dislike,
                                         follow_and_profile, get_media,
                                         no_tweet, tape, template,
                                         users_tweets)


@pytest.mark.anyio
@pytest.mark.app
async def test_fast_api(client, mock_open, mock_get_media_by_id):
    """Тестирует работу приложения"""
    await create_user.test_user_creation(client=client)
    await create_media.test_create_media_file(
        client=client
    )
    logger.info(f"Have use mock: {mock_open}")
    await get_media.test_create_media_file(
        client=client
    )
    logger.info(f"Have use mock: {mock_get_media_by_id}")
    await users_tweets.test_for_tweets(client=client)
    await tape.test_tape_tweets(client=client)
    await follow_and_profile.test_tape_tweets(client=client)
    await template.get_template(client=client, template=template)
    await delete_follow.unsubscribe(client=client)
    await dislike.delete_like(client=client)
    await no_tweet.delete_tweet(client=client)
