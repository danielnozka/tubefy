import logging
import os
import platform
import py7zr

from logging import Logger
from string import Template
from youtube_dl import YoutubeDL

from ..domain.audio_download_options import AudioDownloadOptions
from ..exceptions.audio_download_exception import AudioDownloadException


class YoutubeAudioDownloader:

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _current_directory: str = os.path.dirname(__file__)
    _ffmpeg_windows_binary_files: str = os.path.join(_current_directory, 'ffmpeg.7z')
    _ffmpeg_linux_path: str = '/usr/bin/ffmpeg'
    _max_download_attempts: int = 3
    _default_codec: str = 'mp3'
    _default_bit_rate: int = 96
    _output_template: Template = Template('${file_path}.%(ext)s')
    _ffmpeg_location: str

    def __init__(self):

        self._ffmpeg_location = self._get_ffmpeg_location()

    def download_audio(self, video_id: str, download_directory: str, filename: str,
                       audio_download_options: AudioDownloadOptions | None = None) -> tuple[str, float]:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\', download_directory=\'{download_directory}\', '
                        f'filename=\'{filename}\', {audio_download_options})')

        download_attempt = 1

        while download_attempt <= self._max_download_attempts:

            try:

                downloader_options = self._get_downloader_options(download_directory, filename, audio_download_options)

                with YoutubeDL(downloader_options) as downloader:

                    downloader.download([self._get_audio_recording_url(video_id)])

                output_file = self._get_output_file(download_directory, filename)
                output_file_megabytes = self._get_file_megabytes(output_file)

                self._log.debug(f'End [funcName](video_id=\'{video_id}\', download_directory=\'{download_directory}\', '
                                f'filename=\'{filename}\', {audio_download_options})')

                return output_file, output_file_megabytes

            except Exception as exception:

                self._log.warning(f'Exception found while downloading audio on attempt {download_attempt}',
                                  extra={'exception': f'{exception.__class__.__name__}: {exception}'})

                download_attempt += 1

        else:

            raise AudioDownloadException

    def get_default_codec(self) -> str:

        return self._default_codec

    def _get_ffmpeg_location(self) -> str:

        if platform.system() == 'Windows':

            self._extract_ffmpeg_binary_files()

            return self._current_directory

        elif platform.system() == 'Linux':

            return self._ffmpeg_linux_path

        else:

            self._log.warning('Operative System does not match Windows or Linux. FFMPEG path might cause problems')

            return self._current_directory

    def _extract_ffmpeg_binary_files(self) -> None:

        with py7zr.SevenZipFile(self._ffmpeg_windows_binary_files, mode='r') as z:

            z.extractall(self._current_directory)

    def _get_downloader_options(self, download_directory: str, filename: str,
                                audio_download_options: AudioDownloadOptions | None = None) -> dict:

        output_template = self._get_output_template(download_directory, filename)

        if audio_download_options is None:

            downloader_options = self._get_default_downloader_options(output_template)

        else:

            downloader_options = self._get_custom_downloader_options(output_template, audio_download_options)

        return downloader_options

    def _get_default_downloader_options(self, output_template: str) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': output_template,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self._default_codec,
                    'preferredquality': str(self._default_bit_rate),
                }
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        return options

    def _get_custom_downloader_options(self, output_template: str,
                                       audio_download_options: AudioDownloadOptions) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': output_template,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_download_options.codec,
                    'preferredquality': str(audio_download_options.bit_rate)
                },
                {
                    'key': 'EmbedThumbnail'
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={audio_download_options.title}',
                '-metadata',
                f'artist={audio_download_options.artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True,
            'writethumbnail': True
        }

        return options

    def _get_output_template(self, download_directory: str, filename: str) -> str:

        return self._output_template.substitute(file_path=os.path.join(download_directory, filename))

    def _get_audio_recording_url(self, video_id: str) -> str:

        return self._url_template.substitute(video_id=video_id)

    def _get_output_file(self, download_directory: str, filename: str,
                         audio_download_options: AudioDownloadOptions | None = None) -> str:

        if audio_download_options is None:

            output_file = f'{os.path.join(download_directory, filename)}.{self._default_codec}'

        else:

            output_file = f'{os.path.join(download_directory, filename)}.{audio_download_options.codec}'

        return output_file

    @staticmethod
    def _get_file_megabytes(file_path: str) -> float:

        return os.stat(file_path).st_size / (1024 ** 2)
