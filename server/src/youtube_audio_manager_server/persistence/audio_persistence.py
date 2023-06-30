import logging
import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from uuid import UUID

from ..configuration.app_settings import AppSettings
from ..domain.audio_recording import AudioRecording
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from .audio_context import AudioContext


class AudioPersistence:

    _log = logging.getLogger(__name__)
    _context: AudioContext
    _audio_files_directory: str

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._context = AudioContext()
        self._audio_files_directory = os.path.abspath(app_settings.persistence_settings.audio_files_directory)

        if not self._directory_exists(self._audio_files_directory):

            self._create_directory(self._audio_files_directory)

    def get_audio_files_directory_for_user(self, user_id: UUID) -> str:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\')')
        user_audio_files_directory = os.path.join(self._audio_files_directory, str(user_id))

        if not self._directory_exists(user_audio_files_directory):

            self._create_directory(user_audio_files_directory)

        self._log.debug(f'End [funcName](user_id=\'{user_id}\')')

        return user_audio_files_directory

    def add_audio_recording(self, audio_recording: AudioRecording) -> None:

        self._log.debug(f'Start [funcName]({audio_recording})')
        self._context.add_audio_recording(audio_recording)
        self._log.debug(f'End [funcName]({audio_recording})')

    def get_all_audio_recordings(self, user_id: UUID) -> list[AudioRecording]:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\')')
        result = self._context.get_all_audio_recordings(user_id)
        self._log.debug(f'End [funcName](user_id=\'{user_id}\')')

        return result

    def get_audio_recording_by_video_id(self, user_id: UUID, video_id: str) -> AudioRecording | None:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')
        result = self._context.get_audio_recording_by_video_id(user_id, video_id)
        self._log.debug(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        return result

    def delete_audio_recording(self, audio_recording: AudioRecording) -> None:

        self._log.debug(f'Start [funcName]({audio_recording})')
        self._context.delete_audio_recording(audio_recording)
        self._delete_audio_recording_file(audio_recording)
        self._log.debug(f'End [funcName]({audio_recording})')

    @staticmethod
    def _directory_exists(directory_path: str) -> bool:

        return os.path.isdir(directory_path)

    @staticmethod
    def _create_directory(directory_path: str) -> None:

        os.makedirs(directory_path, exist_ok=True)

    @staticmethod
    def _delete_audio_recording_file(audio_recording: AudioRecording) -> None:

        if os.path.isfile(audio_recording.file):

            os.remove(audio_recording.file)

        else:

            raise AudioFileNotFoundException(audio_recording.file)
