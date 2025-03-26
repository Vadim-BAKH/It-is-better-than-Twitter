"""Удаление лайка"""

import pytest
from fastapi import status


@pytest.mark.app
async def delete_like(client):
    """Тест удаления лайка"""

    response = await client.delete("/api/tweets/2/likes")
    assert response.status_code == status.HTTP_200_OK
    unsubscribe_response = response.json()
    assert unsubscribe_response["result"] is True
