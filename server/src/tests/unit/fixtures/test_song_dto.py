import pytest

from youtube_music_manager_server.domain import Song
from youtube_music_manager_server.dtos import SongDto


@pytest.fixture(scope='package')
def test_song_dto(test_song: Song) -> SongDto:

    return SongDto(id_=test_song.id, title=test_song.title, artist=test_song.artist)
