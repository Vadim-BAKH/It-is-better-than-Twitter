"""Создание пользователей"""

import pytest
from fastapi import status


@pytest.mark.app
async def test_user_creation(client):
    """Тестирует создание пользователей"""
    response = await client.post("/api/users", json={"name": "Dima"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Dima"

    response = await client.post("/api/users", json={"name": "Luda"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Luda"
