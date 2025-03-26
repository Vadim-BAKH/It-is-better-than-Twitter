"""Конфигурация базы данных"""

import re

import pytest
from fast_api.database import (DB_PASSWORD, DB_URI, DB_USER, TEST_DB_URI,
                               async_engine, test_async_engine)


@pytest.mark.config
def test_conf_database():
    """Тестирует конфигурацию баз данных"""
    assert (DB_URI ==
            f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:5432/twitter_db")
    assert (TEST_DB_URI ==
            "postgresql+asyncpg://test:test@localhost:5433/test_db")

    url_str = str(async_engine.url)
    pattern = r"^postgresql\+asyncpg://.*@db:5432/twitter_db$"
    assert re.match(pattern, url_str), "URL движка не соответствует ожидаемому"

    test_url_str = str(test_async_engine.url)
    pattern_test = r"^postgresql\+asyncpg://.*@localhost:5433/test_db$"
    assert re.match(
        pattern_test, test_url_str
    ), "URL тестового движка не соответствует ожидаемому"
