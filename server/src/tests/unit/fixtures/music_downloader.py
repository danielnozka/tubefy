import pytest

from youtube_music_manager_server.use_cases.music_downloader import MusicDownloader


@pytest.fixture(scope='class')
def music_downloader() -> MusicDownloader:

    return MusicDownloader()
