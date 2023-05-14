import pytest

from youtube_music_manager_server.persistence import MusicPersistence


@pytest.fixture(scope='class', autouse=True)
def music_persistence() -> MusicPersistence:

    return MusicPersistence()
