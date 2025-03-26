"""Удаление подписки"""

import pytest
from fastapi import status


@pytest.mark.app
async def unsubscribe(client):
    """Тест отписки от пользователя"""

    response = await client.delete("/api/users/2/follow")
    assert response.status_code == status.HTTP_200_OK
    unsubscribe_response = response.json()
    assert unsubscribe_response["result"] is True
