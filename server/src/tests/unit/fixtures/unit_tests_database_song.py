import pytest

from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.persistence.domain.database_song import DatabaseSong


@pytest.fixture(scope='package')
def unit_tests_database_song(unit_tests_song: Song) -> DatabaseSong:

    song = DatabaseSong(id_=unit_tests_song.id,
                        title=unit_tests_song.title,
                        artist=unit_tests_song.artist,
                        creation_date=unit_tests_song.creation_date.strftime('%d-%m-%Y %H:%M:%S.%f'),
                        file=unit_tests_song.file,
                        file_size_megabytes=unit_tests_song.file_size_megabytes,
                        audio_codec=unit_tests_song.audio_codec,
                        audio_bit_rate=unit_tests_song.audio_bit_rate)

    return song
