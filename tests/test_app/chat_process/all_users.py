"""Все пользователи"""

import pytest
from fastapi import status


@pytest.mark.app
async def see_all_users(client) -> list:
    """Тестирует получение всех пользователей,
    возвращает их список"""
    response = await client.get("/api/users")
    assert response.status_code == status.HTTP_200_OK
    users_response = response.json()
    assert isinstance(users_response, dict)
    assert "users" in users_response
    users = users_response["users"]
    assert isinstance(users, list)
    assert len(users) == 2
    assert users[0]["name"] == "Dima"
    assert users[1]["name"] == "Luda"
    return users
