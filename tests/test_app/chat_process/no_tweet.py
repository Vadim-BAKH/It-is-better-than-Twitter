"""Удаление твита"""

import pytest
from fast_api.logs import logger
from fastapi import status


@pytest.mark.app
async def delete_tweet(client):
    """Тест удаления своего твита и невозможности удаления
    чужого твита"""

    response = await client.delete("/api/tweets/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    no_tweet_response = response.json()
    logger.info(f"no_tweet_response: {no_tweet_response}")
    assert no_tweet_response["detail"]["result"] is False
    assert no_tweet_response["detail"]["error_type"] == "HTTPException"
    assert (no_tweet_response["detail"]["error_message"] ==
            "An attempt to remove someone else's tweet")

    response = await client.delete("/api/tweets/3")
    assert response.status_code == status.HTTP_200_OK
    no_tweet_response = response.json()
    assert no_tweet_response["result"] is True
