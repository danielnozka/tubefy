import pytest

from tubefy.domain.audio_recording import AudioRecording


@pytest.fixture(scope='session')
def test_audio_download_options(test_audio_recording: AudioRecording) -> dict:

    download_options = {
        'title': test_audio_recording.title,
        'artist': test_audio_recording.artist,
        'codec': test_audio_recording.codec.upper(),
        'bitRate': test_audio_recording.bit_rate
    }

    return download_options
