"""Fixtures compartidos para las pruebas de la app de empleados."""

import os

import pytest

URL_API_POR_DEFECTO = "http://localhost:8000"
URL_WEB_POR_DEFECTO = "http://localhost:8080"


@pytest.fixture
def url_api() -> str:
    return os.environ.get("URL_API", URL_API_POR_DEFECTO)


@pytest.fixture
def url_web() -> str:
    return os.environ.get("URL_WEB", URL_WEB_POR_DEFECTO)
