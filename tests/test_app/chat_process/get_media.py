"""Получение медиа файла"""

import pytest
from fastapi import status


@pytest.mark.app
async def test_create_media_file(client):
    """Тест медиа файла по ID"""
    media_id = 1
    response = await client.get(f"/api/medias/{media_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Content-Disposition") is not None
    assert response.headers.get("Content-Type") == "application/octet-stream"
    assert response.content == b"Mocked file content"
