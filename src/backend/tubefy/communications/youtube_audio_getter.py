import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from string import Template
from yt_dlp import YoutubeDL
from ..exceptions.audio_download_exception import AudioDownloadException
from ..settings.app_settings import AppSettings
from ..settings.audio_conversion_settings import AudioConversionSettings


class YoutubeAudioGetter:

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _max_download_attempts: int = 3
    _output_file_template: Template = Template('${output_file_path}.%(ext)s')
    _audio_conversion_settings: AudioConversionSettings

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']) -> None:

        self._audio_conversion_settings = app_settings.audio_conversion_settings

    def _download_audio(self, video_id: str, download_options: dict) -> None:

        with YoutubeDL(download_options) as downloader:

            download_attempt: int = 1

            while download_attempt <= self._max_download_attempts:

                try:

                    downloader.download([self._url_template.substitute(video_id=video_id)])

                    return

                except Exception as exception:

                    self._log.warning(
                        msg=(
                            f'Exception found while downloading audio from video \'{video_id}\' '
                            f'on attempt {download_attempt}'
                        ),
                        extra={'exception': exception}
                    )

                    download_attempt += 1

            else:

                raise AudioDownloadException

    def _get_output_file_template(self, output_directory: Path, output_filename: str) -> str:

        return self._output_file_template.substitute(output_file_path=output_directory.joinpath(output_filename))
