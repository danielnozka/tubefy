import pytest

from youtube_audio_manager_server.domain.audio_recording import AudioRecording


@pytest.fixture(scope='session')
def test_input_audio_recording(test_audio_recording: AudioRecording) -> dict:

    input_data = {
        'title': test_audio_recording.title,
        'artist': test_audio_recording.artist,
        'codec': test_audio_recording.codec.upper(),
        'bitRate': test_audio_recording.bit_rate
    }

    return input_data
