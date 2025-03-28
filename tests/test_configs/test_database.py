"""Конфигурация базы данных"""

import pytest
from fast_api.database import (DB_PASSWORD, DB_PORT, DB_URI, DB_USER,
                               TEST_DB_URI)


@pytest.mark.config
def test_conf_database():
    """Тестирует конфигурацию баз данных"""
    assert (
            DB_URI == f"postgresql+asyncpg:"
                      f"//{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/twitter_db"
    )
    assert (TEST_DB_URI ==
            "postgresql+asyncpg://test:test@localhost:5433/test_db")
