import pytest

from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.dtos.output_song import OutputSong


@pytest.fixture(scope='package')
def unit_tests_output_song(unit_tests_song: Song) -> OutputSong:

    return OutputSong(id_=unit_tests_song.id,
                      title=unit_tests_song.title,
                      artist=unit_tests_song.artist,
                      file_size_megabytes=unit_tests_song.file_size_megabytes,
                      audio_codec=unit_tests_song.audio_codec,
                      audio_bit_rate=unit_tests_song.audio_bit_rate)
