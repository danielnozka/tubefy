import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from string import Template
from uuid import uuid4
from yt_dlp import YoutubeDL

from ..configuration import AppSettings, AudioConversionSettings
from ..domain import AudioRecording, AudioSample, User
from ..dtos import AudioDownloadOptionsInput
from ..exceptions import AudioDownloadException


class YoutubeAudioDownloader:

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _output_file_template: Template = Template('${output_file_path}.%(ext)s')
    _max_download_attempts: int = 3
    _audio_conversion_settings: AudioConversionSettings

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._audio_conversion_settings = app_settings.audio_conversion_settings

    def download_audio_sample(self, video_id: str, output_directory: Path, output_filename: str) -> AudioSample:

        self._log.debug(
            f'Start [funcName](video_id=\'{video_id}\', output_directory=\'{output_directory}\', '
            f'output_file_name=\'{output_filename}\')'
        )
        self._download(
            video_id=video_id,
            download_options=self._get_audio_sample_download_options(
                output_directory=output_directory,
                output_filename=output_filename
            )
        )
        result: AudioSample = AudioSample(
            id_=uuid4(),
            video_id=video_id,
            file_path=self._get_audio_sample_file_path(
                output_directory=output_directory,
                output_filename=output_filename
            )
        )
        self._log.debug(
            f'End [funcName](video_id=\'{video_id}\', output_directory=\'{output_directory}\', '
            f'output_file_name=\'{output_filename}\')'
        )

        return result

    def download_audio_recording(
        self,
        video_id: str,
        output_directory: Path,
        output_filename: str,
        audio_download_options_input: AudioDownloadOptionsInput,
        user: User
    ) -> AudioRecording:

        self._log.debug(
            f'Start [funcName](video_id=\'{video_id}\', output_directory=\'{output_directory}\', '
            f'output_file_name=\'{output_filename}\', audio_download_options_input={audio_download_options_input}, '
            f'user={user})'
        )
        self._download(
            video_id=video_id,
            download_options=self._get_audio_recording_download_options(
                output_directory=output_directory,
                output_filename=output_filename,
                audio_download_options_input=audio_download_options_input
            )
        )
        result: AudioRecording = AudioRecording(
            id_=uuid4(),
            video_id=video_id,
            file_path=self._get_audio_recording_file_path(
                output_directory=output_directory,
                output_filename=output_filename,
                audio_download_options_input=audio_download_options_input
            ),
            title=audio_download_options_input.title,
            artist=audio_download_options_input.artist,
            codec=audio_download_options_input.codec,
            bit_rate=audio_download_options_input.bit_rate,
            user_id=user.id
        )
        self._log.debug(
            f'End [funcName](video_id=\'{video_id}\', output_directory=\'{output_directory}\', '
            f'output_file_name=\'{output_filename}\', audio_download_options_input={audio_download_options_input}, '
            f'user={user})'
        )

        return result

    def _get_audio_sample_download_options(self, output_directory: Path, output_filename: str) -> dict:

        return {
            'ffmpeg_location': self._audio_conversion_settings.ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'nocheckcertificate': True,
            'outtmpl': self._get_output_file_template(
                output_directory=output_directory,
                output_filename=output_filename
            ),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self._audio_conversion_settings.audio_sample_codec,
                    'preferredquality': str(self._audio_conversion_settings.audio_sample_bit_rate),
                }
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

    def _get_audio_recording_download_options(
        self,
        output_directory: Path,
        output_filename: str,
        audio_download_options_input: AudioDownloadOptionsInput
    ) -> dict:

        return {
            'ffmpeg_location': self._audio_conversion_settings.ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'nocheckcertificate': True,
            'outtmpl': self._get_output_file_template(
                output_directory=output_directory,
                output_filename=output_filename
            ),
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

    def _download(self, video_id: str, download_options: dict) -> None:

        with YoutubeDL(download_options) as downloader:

            download_attempt: int = 1

            while download_attempt <= self._max_download_attempts:

                try:

                    downloader.download([self._url_template.substitute(video_id=video_id)])

                    return

                except Exception as exception:

                    self._log.warning(f'Exception found while downloading audio on attempt {download_attempt}',
                                      extra={'exception': exception})

                    download_attempt += 1

            else:

                raise AudioDownloadException

    def _get_output_file_template(self, output_directory: Path, output_filename: str) -> str:

        return self._output_file_template.substitute(output_file_path=output_directory.joinpath(output_filename))

    def _get_audio_sample_file_path(self, output_directory: Path, output_filename: str) -> Path:

        return output_directory.joinpath(f'{output_filename}.{self._audio_conversion_settings.audio_sample_codec}')

    @staticmethod
    def _get_audio_recording_file_path(
        output_directory: Path,
        output_filename: str,
        audio_download_options_input: AudioDownloadOptionsInput
    ) -> Path:

        return output_directory.joinpath(f'{output_filename}.{audio_download_options_input.codec}')
