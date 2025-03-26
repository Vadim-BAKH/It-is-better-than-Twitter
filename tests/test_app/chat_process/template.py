"""Шаблон приложения"""

import pytest
from fast_api.app import app
from fastapi import status
from fastapi.templating import Jinja2Templates


@pytest.mark.app
async def get_template(client, template):
    """Тестирует шаблон приложения"""
    response = await client.get("/api")
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    app.dependency_overrides[Jinja2Templates] = lambda: template
    response = await client.get("/api/")
    assert response.status_code == status.HTTP_200_OK
