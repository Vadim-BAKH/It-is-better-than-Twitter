"""Конфигуратор тестов"""

from typing import AsyncGenerator

import pytest
from fast_api.app import app
from fast_api.business_model.models import Base
from fast_api.database import (get_session_db, test_async_engine,
                               test_async_session)
from fast_api.logs import logger
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True)
async def override_dependencies():
    """Переопределяет основную сессию
    на тестовую"""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        """Создает сессию для тестов"""
        async with test_async_session() as session:
            yield session

    app.dependency_overrides[get_session_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def test_database() -> AsyncGenerator:
    """Фикстура для управления миграциями"""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield

    finally:
        async with test_async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_async_engine.dispose()


@pytest.fixture
async def client():
    """Возвращает асинхронный клиент"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def template() -> Jinja2Templates:
    """Возвращает шаблоны Jinja2"""
    return Jinja2Templates(directory="fast_api/templates")


@pytest.fixture
def mock_open(mocker):
    """Мокирует функцию `aiofiles.open`,
     чтобы избежать реального открытия файлов."""
    mocker.patch("aiofiles.open")
    yield


@pytest.fixture
def mock_get_media_by_id(mocker):
    """Мокирует функцию `see_media_by_id`,
     чтобы вернуть заранее заданный ответ."""
    async def mock_return(*args, **kwargs):
        mock_content = b"Mocked file content"
        mock_headers = {
            "Content-Disposition": "attachment; filename=example.jpg",
            "Content-Type": "application/octet-stream",
        }
        logger.info(f"*args: {args}, **kwargs: {kwargs}")
        return Response(
            content=mock_content,
            status_code=200,
            headers=mock_headers
        )

    mocker.patch(
        "fast_api.business_model.services.media.get_media_bt.see_media_by_id",
        side_effect=mock_return,
    )
    yield

# @pytest.fixture
# def mock_exists(mocker):
#     """ Мокирует функцию `os.path.exists`,
#      чтобы она всегда возвращала `True`."""
#     mocker.patch("os.path.exists", return_value=True)
#     yield

# @pytest.fixture
# def mock_stat(mocker):
#     """Мокирует функцию `os.stat`,
#      чтобы вернуть заранее заданные значения."""
#     mock_stat_result = MagicMock(st_size=1024, st_mode=0o100644)
#     mocker.patch("os.stat", return_value=mock_stat_result)
#     yield


# @pytest.fixture
# def mock_mimetypes(mocker):
#     """Мокирует модуль `mimetypes`
#     и его базу данных MIME-типов."""
#
#     # Создаем мок-объект базы данных mimetypes
#     mock_db = MagicMock()
#     # Возвращаем нужный MIME-тип
#     mock_db.guess_type.return_value = ("image/jpeg", None)
#
#     # Мокируем весь модуль mimetypes
#     mocker.patch.object(mimetypes, "MimeTypes", return_value=mock_db)
#
#     # Перезагружаем модуль с новой конфигурацией
#     mimetypes.init()
#     yield
