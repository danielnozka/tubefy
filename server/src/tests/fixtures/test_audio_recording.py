import os
import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_audio_manager_server.configuration.app_settings import AppSettings
from youtube_audio_manager_server.domain.audio_recording import AudioRecording


@pytest.fixture(scope='session')
@inject
def test_audio_recording(app_settings: AppSettings = Provide['app_settings']) -> AudioRecording:

    audio_recording_id = 'dQw4w9WgXcQ'
    audio_recording_title = 'Never gonna give you up'
    audio_recording_artist = 'Rick Astley'
    audio_recording_codec = 'mp3'
    audio_recording_bit_rate = 320
    audio_files_absolute_directory = os.path.abspath(app_settings.persistence_settings.audio_files_directory)
    audio_recording_file = os.path.join(audio_files_absolute_directory,
                                        f'{audio_recording_artist} - {audio_recording_title}.{audio_recording_codec}')
    audio_recording_file_size_megabytes = 0.0

    audio_recording = AudioRecording(id_=audio_recording_id,
                                     title=audio_recording_title,
                                     artist=audio_recording_artist,
                                     file=audio_recording_file,
                                     file_size_megabytes=audio_recording_file_size_megabytes,
                                     codec=audio_recording_codec,
                                     bit_rate=audio_recording_bit_rate)

    return audio_recording
