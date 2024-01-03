import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from uuid import UUID

from ..domain import User
from ..exceptions import AudioRecordingNotFoundException
from ..persistence import AudioRecordingsPersistence


class AudioRecordingDeleter:

    _log: Logger = logging.getLogger(__name__)
    _audio_recordings_persistence: AudioRecordingsPersistence

    @inject
    def __init__(
        self,
        audio_recordings_persistence: AudioRecordingsPersistence = Provide['audio_recordings_persistence']
    ):

        self._audio_recordings_persistence = audio_recordings_persistence

    def delete(self, audio_recording_id: UUID, user: User) -> None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')
        audio_recording = next((x for x in user.audio_recordings if x.id == audio_recording_id), None)

        if audio_recording is None:

            raise AudioRecordingNotFoundException(audio_recording_id)

        else:

            database_audio_recording = self._audio_recordings_persistence.get_audio_recording(audio_recording_id)
            self._audio_recordings_persistence.delete_audio_recording(database_audio_recording)
            self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')
