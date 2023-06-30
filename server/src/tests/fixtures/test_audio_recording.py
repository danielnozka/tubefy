import os
import pytest

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from uuid import uuid4

from youtube_audio_manager_server.configuration.app_settings import AppSettings
from youtube_audio_manager_server.domain.audio_recording import AudioRecording


@pytest.fixture(scope='session')
@inject
def test_audio_recording(app_settings: AppSettings = Provide['app_settings']) -> AudioRecording:

    video_id = 'dQw4w9WgXcQ'
    user_id = uuid4()
    title = 'Never gonna give you up'
    artist = 'Rick Astley'
    codec = 'mp3'
    bit_rate = 320
    audio_files_absolute_directory = os.path.abspath(app_settings.persistence_settings.audio_files_directory)
    file = os.path.join(audio_files_absolute_directory, str(user_id), f'{artist} - {title}.{codec}')
    file_size_megabytes = 0.0

    audio_recording = AudioRecording(id_=uuid4(),
                                     video_id=video_id,
                                     user_id=user_id,
                                     title=title,
                                     artist=artist,
                                     file=file,
                                     file_size_megabytes=file_size_megabytes,
                                     codec=codec,
                                     bit_rate=bit_rate)

    return audio_recording
