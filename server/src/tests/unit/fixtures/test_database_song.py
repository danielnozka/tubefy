import pytest

from youtube_music_manager_server.domain import Song
from youtube_music_manager_server.persistence.domain import DatabaseSong


@pytest.fixture(scope='package')
def test_database_song(test_song: Song) -> DatabaseSong:

    song = DatabaseSong(id_=test_song.id,
                        title=test_song.title,
                        artist=test_song.artist,
                        creation_date=test_song.creation_date.strftime('%d-%m-%Y %H:%M:%S.%f'),
                        file=test_song.file)

    return song
