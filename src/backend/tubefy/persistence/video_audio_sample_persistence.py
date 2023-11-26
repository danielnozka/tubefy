import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from string import Template

from ..configuration import AppSettings, AudioConversionSettings
from ..domain import VideoAudioSample
from ..services import DirectoryBuilder


class VideoAudioSamplePersistence:

    _log: Logger = logging.getLogger(__name__)
    _sample_files_directory: str = 'samples'
    _sample_files_directory_path: Path
    _sample_file_path_template: Template
    _audio_conversion_settings: AudioConversionSettings

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_builder: DirectoryBuilder = Provide['directory_builder']
    ):

        self._sample_files_directory_path = directory_builder.build(
            app_settings.persistence_settings.audio_files_directory_path.joinpath(self._sample_files_directory)
        )
        self._audio_conversion_settings = app_settings.audio_conversion_settings
        self._sample_file_path_template = Template(f'${{file_path}}.{self._audio_conversion_settings.default_codec}')

    def get_video_audio_sample(self, video_id: str) -> VideoAudioSample:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        result = VideoAudioSample(video_id=video_id, file_path=self._get_video_audio_sample_file_path(video_id))
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

    @staticmethod
    def video_audio_sample_exists(video_audio_sample: VideoAudioSample) -> bool:

        return video_audio_sample.file_path.exists()

    def _get_video_audio_sample_file_path(self, video_id: str) -> Path:

        return self._sample_files_directory_path.joinpath(
            self._sample_file_path_template.substitute(file_path=video_id)
        )
