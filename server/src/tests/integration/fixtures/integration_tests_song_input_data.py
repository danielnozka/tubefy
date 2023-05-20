import pytest

from youtube_music_manager_server.domain.song import Song


@pytest.fixture(scope='package')
def integration_tests_song_input_data(integration_tests_song: Song) -> dict:

    input_data = {
        'title': integration_tests_song.title,
        'artist': integration_tests_song.artist,
        'audioCodec': integration_tests_song.audio_codec.upper(),
        'audioBitRate': integration_tests_song.audio_bit_rate
    }

    return input_data
