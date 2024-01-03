import pytest

from dependency_injector.wiring import inject, Provide
from fastapi.testclient import TestClient

from tubefy import App
from tubefy.configuration import AppSettings


@pytest.fixture(scope='session')
@inject
def test_client(app_settings: AppSettings = Provide['app_settings']) -> TestClient:

    return TestClient(App(host=app_settings.server_settings.host, port=app_settings.server_settings.port))
