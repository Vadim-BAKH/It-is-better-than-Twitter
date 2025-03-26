"""Загрузка медиа файла"""


import pytest
from fastapi import status

from tests.factories_tests.load_media_test import load_media


@pytest.mark.app
async def test_create_media_file(client):
    """Тест загрузки медиафайла"""
    response = await client.post("/api/medias", files=await load_media())
    assert response.status_code == status.HTTP_201_CREATED
    media_response = response.json()
    assert isinstance(media_response, dict)
    assert media_response["result"] is True
    assert isinstance(media_response["media_id"], int)
