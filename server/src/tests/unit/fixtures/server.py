import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server import Server
from youtube_music_manager_server.configuration import AppSettings


@pytest.fixture(scope='class')
@inject
def server(app_settings: AppSettings = Provide['app_settings']) -> Server:

    return Server(app_settings.root_path, app_settings.server_settings.host, app_settings.server_settings.port)
