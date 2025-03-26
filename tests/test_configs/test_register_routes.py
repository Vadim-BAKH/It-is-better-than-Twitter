"""Тесты конфигурации маршрутов"""

import pytest
from fast_api.register_routes import router, templates
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates


@pytest.mark.config
def test_templates_configuration():
    """Конфигурация шаблона"""
    assert isinstance(templates, Jinja2Templates)


@pytest.mark.config
def test_router_configuration():
    """Конфигурация router"""
    assert isinstance(router, APIRouter)
    assert router.prefix == "/api"
    assert router.tags == ["twitter"]


@pytest.mark.config
def test_routes_exist():
    """Количество router"""
    assert len(router.routes) == 18


@pytest.mark.config
@pytest.mark.parametrize(
    "route_name",
    [
        "/api/",
        "/api/users",
        "/api/users/me",
        "/api/tweets",
        "/api/medias",
        "/api/users/{idu}",
        "/api/medias/{media_id}",
        "/api/tweets/{idt}/likes",
        "/api/tweets/{idt}",
        "/api/users/{idu}/follow",
    ],
)
def test_specific_routes(route_name):
    """Наличие маршрутов"""
    found = any(route.path == route_name for route in router.routes)
    assert found, f"Маршрут {route_name} не найден"
