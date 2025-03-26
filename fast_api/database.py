"""Для запуска сессии с базой данных"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from fast_api.secret_mission.conf_env import DB_PASSWORD, DB_USER

DB_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:5432/twitter_db"

TEST_DB_URI = "postgresql+asyncpg://test:test@localhost:5433/test_db"

async_engine = create_async_engine(DB_URI)

test_async_engine = create_async_engine(TEST_DB_URI)


async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False
)
test_async_session = async_sessionmaker(
    bind=test_async_engine, expire_on_commit=False
)


async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    """Запускает асинхронную сессию"""
    async with async_session() as session:
        yield session
