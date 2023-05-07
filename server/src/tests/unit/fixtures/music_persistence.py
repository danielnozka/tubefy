import pytest

from youtube_music_manager_server.persistence.music_persistence import MusicPersistence


@pytest.fixture
def music_persistence() -> MusicPersistence:

    return MusicPersistence()
