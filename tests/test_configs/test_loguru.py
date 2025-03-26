"""Конфигурация логирования"""

from pathlib import Path

import pytest
from fast_api.logs import logger


@pytest.mark.config
def test_logging_configuration():
    """Тест логирования"""
    assert logger.level("INFO")
    log_file = Path("loguru/twitter.log")

    logger.info("Let's test loguru")

    assert log_file.exists()
    with open("loguru/twitter.log", mode="r", encoding="utf-8") as file:
        log_content = file.read()
        assert "Let's test loguru" in log_content, "Loguru don't work"
