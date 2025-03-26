"""Профиль пользователей"""


import pytest
from fastapi import status

from tests.test_app.chat_process.all_users import see_all_users


@pytest.mark.app
async def test_tape_tweets(client):
    """Подписываемся на пользователей,
    получаем профили"""

    users = await see_all_users(client=client)

# Dima подписывается на Luda
    response = await client.post("/api/users/2/follow")
    assert response.status_code == status.HTTP_201_CREATED
    follow_response = response.json()
    assert follow_response["result"] is True

    # Luda подписывается на Dima
    response = await client.post(
        "/api/users/1/follow_fiction",
        json={"api_key": f"{users[1]["api_key"]}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    follow_response = response.json()
    assert follow_response["result"] is True

    # Профиль Dima
    response = await client.get("/api/users/me")
    assert response.status_code == status.HTTP_200_OK
    me_response = response.json()
    assert me_response["result"] is True
    assert me_response["user"]["id"] == 1
    assert me_response["user"]["name"] == "Dima"
    followers = me_response["user"]["followers"]
    following = me_response["user"]["following"]
    assert followers[0]["id"] == 2
    assert followers[0]["name"] == "Luda"
    assert following[0]["id"] == 2
    assert following[0]["name"] == "Luda"

    # Профиль Luda
    response = await client.get("/api/users/2")
    assert response.status_code == status.HTTP_200_OK
    prof_response = response.json()
    assert prof_response["result"] is True
    assert prof_response["user"]["id"] == 2
    assert prof_response["user"]["name"] == "Luda"
    followers = prof_response["user"]["followers"]
    following = prof_response["user"]["following"]
    assert followers[0]["id"] == 1
    assert followers[0]["name"] == "Dima"
    assert following[0]["id"] == 1
    assert following[0]["name"] == "Dima"
