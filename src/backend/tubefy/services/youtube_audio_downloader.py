import logging
from logging import Logger
from string import Template
from yt_dlp import YoutubeDL
from ..domain.audio import Audio
from ..domain.audio_download_options import AudioDownloadOptions
from .i_audio_downloader import IAudioDownloader


class YoutubeAudioDownloader(IAudioDownloader):

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _max_download_attempts: int = 3
    _output_file_template: Template = Template('${output_file_path}.%(ext)s')

    def __init__(self) -> None:

        pass

    def download_audio(self, audio_download_options: AudioDownloadOptions) -> Audio:

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
