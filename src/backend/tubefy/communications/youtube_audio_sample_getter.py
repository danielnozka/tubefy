import logging
from logging import Logger
from pathlib import Path
from uuid import uuid4
from .youtube_audio_getter import YoutubeAudioGetter
from ..domain.audio_sample import AudioSample


class YoutubeAudioSampleGetter(YoutubeAudioGetter):

    _log: Logger = logging.getLogger(__name__)

    def get(self, video_id: str, output_directory: Path, output_filename: str) -> AudioSample:

        self._log.debug(
            f'Start [funcName](video_id=\'{video_id}\', output_directory=\'{output_directory}\', '
            f'output_file_name=\'{output_filename}\')'
        )
        self._download_audio(
            video_id=video_id,
            download_options=self._get_download_options(
                output_directory=output_directory,
                output_filename=output_filename
            )
        )
        result: AudioSample = AudioSample(
            id=uuid4(),
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

    def _get_download_options(self, output_directory: Path, output_filename: str) -> dict:

        return {
            'ffmpeg_location': self._audio_conversion_settings.ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'logger': self._log,
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
            'prefer_ffmpeg': True
        }

    def _get_audio_sample_file_path(self, output_directory: Path, output_filename: str) -> Path:

        return output_directory.joinpath(f'{output_filename}.{self._audio_conversion_settings.audio_sample_codec}')
