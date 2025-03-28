"""Приложение FastApi"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI

from fast_api.business_model.models import Base
from fast_api.database import async_engine
from fast_api.logs import logger
from fast_api.register_routes import router as tasks_router
from fast_api.secret_mission.conf_env import SENTRY_DSN


@asynccontextmanager
async def database_life_cycle(api: FastAPI) -> AsyncIterator:
    """Устанавливает и закрывает асинхронное
    соединение с базой движка, создает таблицы
    моделей, если их нет"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Tables are successfully created with {api}")
    yield
    await async_engine.dispose()

# Инициализация Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
)

app = FastAPI(lifespan=database_life_cycle)

app.include_router(tasks_router)
