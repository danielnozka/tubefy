import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path

from ..configuration import AppSettings
from .database_context import DatabaseContext
from .domain import DatabaseAudioSample
from ..services import DirectoryHandler


class AudioSamplesPersistence:

    _log: Logger = logging.getLogger(__name__)
    _sample_files_directory: str = 'samples'
    _database_context: DatabaseContext
    _sample_files_directory_path: Path

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_handler: DirectoryHandler = Provide['directory_handler']
    ):

        self._database_context = DatabaseContext(
            directory_handler.create_directory(app_settings.persistence_settings.data_path)
        )
        self._sample_files_directory_path = directory_handler.create_directory(
            app_settings.persistence_settings.data_path.joinpath(self._sample_files_directory)
        )

    def close(self) -> None:

        self._database_context.close()

    def get_audio_sample(self, video_id: str) -> DatabaseAudioSample | None:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        result = self._database_context.get_audio_sample(video_id)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

    def add_audio_sample(self, database_audio_sample: DatabaseAudioSample) -> None:

        self._log.debug(f'Start [funcName](database_audio_sample={database_audio_sample})')
        self._database_context.add_audio_sample(database_audio_sample)
        self._log.debug(f'End [funcName](database_audio_sample={database_audio_sample})')

    def get_audio_samples_directory(self) -> Path:

        return self._sample_files_directory_path

    @staticmethod
    def get_audio_sample_filename(video_id: str) -> str:

        return video_id
