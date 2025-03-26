"""Тест app"""

import pytest
from fast_api.app import app
from fastapi import FastAPI


@pytest.mark.config
def test_app_configuration():
    """Тестирует app"""
    assert isinstance(app, FastAPI)
