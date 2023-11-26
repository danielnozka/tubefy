import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from string import Template
from yt_dlp import YoutubeDL

from ..configuration import AppSettings, AudioConversionSettings
from ..domain import BaseVideoAudio
from ..dtos import AudioDownloadOptionsInput
from ..exceptions import AudioDownloadException


class YoutubeAudioDownloader:

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _max_download_attempts: int = 3
    _output_template: Template = Template('${file_path_without_extension}.%(ext)s')
    _audio_conversion_settings: AudioConversionSettings

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._audio_conversion_settings = app_settings.audio_conversion_settings

    def download(
        self,
        video_audio: BaseVideoAudio,
        audio_download_options_input: AudioDownloadOptionsInput | None = None
    ) -> None:

        self._log.debug(f'Start [funcName]({video_audio}, {audio_download_options_input})')

        download_attempt = 1

        while download_attempt <= self._max_download_attempts:

            try:

                downloader_options = self._get_downloader_options(video_audio, audio_download_options_input)

                with YoutubeDL(downloader_options) as downloader:

                    downloader.download([self._get_audio_recording_url(video_audio.video_id)])

                self._log.debug(f'End [funcName]({video_audio}, {audio_download_options_input})')

                return

            except Exception as exception:

                self._log.warning(f'Exception found while downloading audio on attempt {download_attempt}',
                                  extra={'exception': exception})

                download_attempt += 1

        else:

            raise AudioDownloadException

    def _get_downloader_options(
        self,
        video_audio: BaseVideoAudio,
        audio_download_options_input: AudioDownloadOptionsInput | None = None
    ) -> dict:

        output_template = self._get_output_template(video_audio)

        if audio_download_options_input is None:

            downloader_options = self._get_default_downloader_options(output_template)

        else:

            downloader_options = self._get_custom_downloader_options(output_template, audio_download_options_input)

        return downloader_options

    def _get_default_downloader_options(self, output_template: str) -> dict:

        options = {
            'ffmpeg_location': self._audio_conversion_settings.ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'logger': self._log,
            'nocheckcertificate': True,
            'outtmpl': output_template,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self._audio_conversion_settings.default_codec,
                    'preferredquality': str(self._audio_conversion_settings.default_bit_rate),
                }
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        return options

    def _get_custom_downloader_options(
        self, output_template: str,
        audio_download_options_input: AudioDownloadOptionsInput
    ) -> dict:

        options = {
            'ffmpeg_location': self._audio_conversion_settings.ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'logger': self._log,
            'nocheckcertificate': True,
            'outtmpl': output_template,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_download_options_input.codec,
                    'preferredquality': str(audio_download_options_input.bit_rate)
                },
                {
                    'key': 'EmbedThumbnail'
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={audio_download_options_input.title}',
                '-metadata',
                f'artist={audio_download_options_input.artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True,
            'writethumbnail': True
        }

        return options

    def _get_output_template(self, video_audio: BaseVideoAudio) -> str:

        return self._output_template.substitute(
            file_path_without_extension=video_audio.file_path.parent.joinpath(video_audio.file_path.stem)
        )

    def _get_audio_recording_url(self, video_id: str) -> str:

        return self._url_template.substitute(video_id=video_id)
