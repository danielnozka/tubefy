import pytest

from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.dtos.input_song import InputSong


@pytest.fixture(scope='package')
def unit_tests_input_song(unit_tests_song: Song) -> InputSong:

    return InputSong(id_=unit_tests_song.id,
                     title=unit_tests_song.title,
                     artist=unit_tests_song.artist,
                     audio_codec=unit_tests_song.audio_codec,
                     audio_bit_rate=unit_tests_song.audio_bit_rate)
