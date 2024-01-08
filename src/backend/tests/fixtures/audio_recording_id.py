import pytest

from dependency_injector.wiring import inject, Provide
from uuid import UUID

from tubefy.domain import AudioRecording, User
from tubefy.use_cases import UserGetter


@pytest.fixture(scope='session')
@inject
def audio_recording_id(json_web_token: str, user_getter: UserGetter = Provide['user_getter']) -> UUID:

    user: User = user_getter.get(json_web_token)
    audio_recording: AudioRecording = user.audio_recordings[0]

    return audio_recording.id
