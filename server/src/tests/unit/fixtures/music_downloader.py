import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.use_cases.music_downloader import MusicDownloader


@pytest.fixture
@inject
def music_downloader(app_settings: AppSettings = Provide['app_settings']) -> MusicDownloader:

    return MusicDownloader(app_settings)
