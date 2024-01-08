import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from uuid import UUID

from ..configuration import AppSettings
from ..domain import User
from ..dtos import AudioDownloadOptionsInput
from .database_context import DatabaseContext
from .domain import DatabaseAudioRecording
from ..services import DirectoryHandler


class AudioRecordingsPersistence:

    _log: Logger = logging.getLogger(__name__)
    _audio_recordings_directory: str = 'recordings'
    _database_context: DatabaseContext
    _directory_handler: DirectoryHandler
    _audio_recordings_directory_path: Path

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_handler: DirectoryHandler = Provide['directory_handler']
    ):

        self._database_context = DatabaseContext(
            directory_handler.create_directory(app_settings.persistence_settings.data_path)
        )
        self._audio_recordings_directory_path = directory_handler.create_directory(
            app_settings.persistence_settings.data_path.joinpath(self._audio_recordings_directory)
        )
        self._directory_handler = directory_handler

    def close(self) -> None:

        self._database_context.close()

    def get_audio_recording(self, audio_recording_id: UUID) -> DatabaseAudioRecording | None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')
        result: DatabaseAudioRecording | None = self._database_context.get_audio_recording(audio_recording_id)
        self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        return result

    def add_audio_recording(self, database_audio_recording: DatabaseAudioRecording) -> None:

        self._log.debug(f'Start [funcName](database_audio_recording={database_audio_recording})')
        self._database_context.add_audio_recording(database_audio_recording)
        self._log.debug(f'End [funcName](database_audio_recording={database_audio_recording})')

    def delete_audio_recording(self, database_audio_recording: DatabaseAudioRecording) -> None:

        self._log.debug(f'Start [funcName](database_audio_recording={database_audio_recording})')
        database_audio_recording_file_path: Path = Path(database_audio_recording.file_path)

        if database_audio_recording_file_path.is_file():

            database_audio_recording_file_path.unlink()

        self._database_context.delete_audio_recording(database_audio_recording)
        self._log.debug(f'End [funcName](database_audio_recording={database_audio_recording})')

    def get_user_audio_recordings_directory(self, user: User) -> Path:

        return self._directory_handler.create_directory(self._audio_recordings_directory_path.joinpath(str(user.id)))

    @staticmethod
    def get_audio_recording_filename(audio_download_options_input: AudioDownloadOptionsInput) -> str:

        return f'{audio_download_options_input.artist} - {audio_download_options_input.title}'
