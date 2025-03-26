"""Конфигурация логирования"""

from loguru import logger

logger.add(
    "loguru/twitter.log",
    level="INFO",
    format="{time}**{level}**{message}",
    rotation="25 MB",
)
