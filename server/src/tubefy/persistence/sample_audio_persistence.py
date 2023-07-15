import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..communications.youtube_audio_downloader import YoutubeAudioDownloader
from ..configuration.app_settings import AppSettings


class SampleAudioPersistence:

    _sample_files_directory: str = 'samples'
    _sample_files_directory_path: str
    _youtube_audio_downloader: YoutubeAudioDownloader

    @inject
    def __init__(self,
                 app_settings: AppSettings = Provide['app_settings'],
                 youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader']):

        self._sample_files_directory_path = os.path.join(
            os.path.abspath(app_settings.persistence_settings.audio_files_directory),
            self._sample_files_directory
        )

        if not self._directory_exists(self._sample_files_directory_path):

            self._create_directory(self._sample_files_directory_path)

        self._youtube_audio_downloader = youtube_audio_downloader

    def get_sample_files_directory(self) -> str:

        return self._sample_files_directory_path

    def get_sample_audio_file(self, video_id: str) -> str | None:

        sample_audio_file = os.path.join(self._sample_files_directory_path,
                                         f'{video_id}.{self._youtube_audio_downloader.get_default_codec()}')

        if os.path.isfile(sample_audio_file):

            return sample_audio_file

        else:

            return None

    @staticmethod
    def _directory_exists(directory_path: str) -> bool:

        return os.path.isdir(directory_path)

    @staticmethod
    def _create_directory(directory_path: str) -> None:

        os.makedirs(directory_path, exist_ok=True)
