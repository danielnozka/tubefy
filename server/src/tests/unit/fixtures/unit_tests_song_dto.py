import pytest

from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.dtos.song_dto import SongDto


@pytest.fixture(scope='package')
def unit_tests_song_dto(unit_tests_song: Song) -> SongDto:

    return SongDto(id_=unit_tests_song.id, title=unit_tests_song.title, artist=unit_tests_song.artist)
