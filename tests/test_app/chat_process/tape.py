"""Лента твитов"""

import pytest
from fastapi import status


@pytest.mark.app
async def test_tape_tweets(client):
    """Получаем ссылку на меди,
    получаем ленту твитов"""

    # Получаем ссылку на медиа файл
    response = await client.get("/api/media_url/1")
    assert response.status_code == status.HTTP_200_OK
    media_link_response = response.json()
    media_link = media_link_response["media_url"]
    assert isinstance(media_link, str)

    # Получаем ленту с порядком твитов
    # по количеству лайков
    response = await client.get("/api/tweets")
    assert response.status_code == status.HTTP_200_OK
    tape_tweets = response.json()
    assert tape_tweets["result"] is True
    tweet1 = tape_tweets["tweets"][0]
    tweet2 = tape_tweets["tweets"][1]
    tweet3 = tape_tweets["tweets"][2]
    assert tweet1["id"] == 2
    assert tweet2["id"] == 1
    assert tweet3["id"] == 3
    assert tweet1["content"] == "How are you: test"
    assert tweet1["attachments"][0] == media_link
