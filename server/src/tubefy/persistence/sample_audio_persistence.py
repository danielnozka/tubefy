import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..configuration.app_settings import AppSettings


class SampleAudioPersistence:

    _sample_files_directory: str = 'samples'
    _sample_files_directory_path: str

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._sample_files_directory_path = os.path.join(
            os.path.abspath(app_settings.persistence_settings.audio_files_directory),
            self._sample_files_directory
        )

        if not self._directory_exists(self._sample_files_directory_path):

            self._create_directory(self._sample_files_directory_path)

    def get_sample_files_directory(self) -> str:

        return self._sample_files_directory_path

    @staticmethod
    def _directory_exists(directory_path: str) -> bool:

        return os.path.isdir(directory_path)

    @staticmethod
    def _create_directory(directory_path: str) -> None:

        os.makedirs(directory_path, exist_ok=True)
