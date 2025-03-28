"""Виртуальное окружение"""

import os

from dotenv import load_dotenv

from fast_api.logs import logger

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
SENTRY_DSN = os.getenv("SENTRY_DSN")

MAIN_USER = 1

if not all(["DB_PASSWORD", "DB_USER", "DB_PORT"]):
    logger.error("Не все переменные окружения загружены из .env")
    raise ValueError("Ошибка виртуального окружения с .env")

logger.info("Установлено виртуальное окружение")
