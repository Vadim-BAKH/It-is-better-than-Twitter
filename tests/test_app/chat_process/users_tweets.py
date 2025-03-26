"""Манипуляции с твитами"""

import pytest
from fastapi import status

from tests.factories_tests.request_templates import (TWEET_AND_MEDIA,
                                                     TWEET_WITHOUT_MEDIA)
from tests.test_app.chat_process.all_users import see_all_users


@pytest.mark.app
async def test_for_tweets(client):
    """Тест  твитов и лайков"""

    users = await see_all_users(client=client)

    # Пользователь Luda отправляет твит
    # с медиа
    response = await client.post(
        "/api/tweets_fiction",
        json={
            "tweet_data": "Fine, OK: test",
            "tweet_media_ids": [1],
            "api_key": f"{users[1]["api_key"]}",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    tweet_response = response.json()
    assert tweet_response["result"] is True
    assert tweet_response["tweet_id"] == 1

    # Пользователь Dima отправляет твит с медиа файлом
    response = await client.post("/api/tweets", json=TWEET_AND_MEDIA)
    assert response.status_code == status.HTTP_201_CREATED
    tweet_response = response.json()
    assert tweet_response["result"] is True
    assert tweet_response["tweet_id"] == 2

    # Пользователь Dima отправляет твит без медиа файла
    response = await client.post("/api/tweets", json=TWEET_WITHOUT_MEDIA)
    assert response.status_code == status.HTTP_201_CREATED
    tweet_response = response.json()
    assert tweet_response["result"] is True
    assert tweet_response["tweet_id"] == 3

    # Dima ставит лайк первому твиту
    response = await client.post("/api/tweets/1/likes")
    assert response.status_code == status.HTTP_201_CREATED
    like_response = response.json()
    assert like_response["result"] is True

    # Dima ставит лайк второму твиту
    response = await client.post("/api/tweets/2/likes")
    assert response.status_code == status.HTTP_201_CREATED
    like_response = response.json()
    assert like_response["result"] is True

    # Luda ставит лайк второму твиту
    response = await client.post(
        "/api/tweets/2/like_fiction",
        json={"api_key": f"{users[1]["api_key"]}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    like_response = response.json()
    assert like_response["result"] is True
