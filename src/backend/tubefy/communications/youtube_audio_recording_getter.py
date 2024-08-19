import logging
from logging import Logger
from pathlib import Path
from uuid import uuid4
from .youtube_audio_getter import YoutubeAudioGetter
from ..domain.audio_recording import AudioRecording
from ..domain.old_user import User
from ..dtos.audio_download_options_input import AudioDownloadOptionsInput


class YoutubeAudioRecordingGetter(YoutubeAudioGetter):

    _log: Logger = logging.getLogger(__name__)

    def get(
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
        self._download_audio(
            video_id=video_id,
            download_options=self._get_download_options(
                output_directory=output_directory,
                output_filename=output_filename,
                audio_download_options_input=audio_download_options_input
            )
        )
        result: AudioRecording = AudioRecording(
            id=uuid4(),
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

    def _get_download_options(
        self,
        output_directory: Path,
        output_filename: str,
        audio_download_options_input: AudioDownloadOptionsInput
    ) -> dict:

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
            'writethumbnail': True
        }

    @staticmethod
    def _get_audio_recording_file_path(
        output_directory: Path,
        output_filename: str,
        audio_download_options_input: AudioDownloadOptionsInput
    ) -> Path:

        return output_directory.joinpath(f'{output_filename}.{audio_download_options_input.codec}')
