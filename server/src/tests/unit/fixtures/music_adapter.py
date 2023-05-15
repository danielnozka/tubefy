import pytest

from youtube_music_manager_server.adapters.music_adapter import MusicAdapter


@pytest.fixture(scope='class')
def music_adapter() -> MusicAdapter:

    return MusicAdapter()
