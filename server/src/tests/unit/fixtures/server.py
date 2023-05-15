import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.server import Server


@pytest.fixture(scope='class')
@inject
def server(app_settings: AppSettings = Provide['app_settings']) -> Server:

    return Server(app_settings.root_path, app_settings.server_settings.host, app_settings.server_settings.port)
