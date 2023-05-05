import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from .fixtures.exposed_test_controller import ExposedTestController
from .fixtures.non_exposed_test_controller import NonExposedTestController
from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.server import Server


@pytest.fixture
def exposed_test_controller() -> ExposedTestController:

    return ExposedTestController()


@pytest.fixture
def non_exposed_test_controller() -> NonExposedTestController:

    return NonExposedTestController()


@pytest.fixture(scope='class')
@inject
def server(app_settings: AppSettings = Provide['app_settings']) -> Server:

    return Server(app_settings.root_path, app_settings.server_settings.host, app_settings.server_settings.port)
