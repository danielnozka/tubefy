import logging
import os
import platform
import py7zr

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from string import Template
from uuid import UUID
from uuid import uuid4
from youtube_dl import YoutubeDL

from ..domain.audio_recording import AudioRecording
from ..dtos.input_audio_recording_options import InputAudioRecordingOptions
from ..exceptions.audio_download_exception import AudioDownloadException
from ..persistence.audio_persistence import AudioPersistence


class AudioDownloader:

    _log: Logger = logging.getLogger(__name__)
    _url_template: Template = Template('https://www.youtube.com/watch?v=${video_id}')
    _current_directory: str = os.path.dirname(__file__)
    _ffmpeg_windows_binary_files: str = os.path.join(_current_directory, 'ffmpeg.7z')
    _ffmpeg_linux_path: str = '/usr/bin/ffmpeg'
    _max_download_attempts: int = 3
    _audio_persistence: AudioPersistence
    _ffmpeg_location: str
    _file_template: Template

    @inject
    def __init__(self, audio_persistence: AudioPersistence = Provide['audio_persistence']):

        self._audio_persistence = audio_persistence
        self._ffmpeg_location = self._get_ffmpeg_location()
        self._file_template = Template('${audio_recording_artist} - ${audio_recording_title}.%(ext)s')

    def download_audio_recording(self, user_id: UUID, video_id: str,
                                 input_audio_recording_options: InputAudioRecordingOptions) -> AudioRecording:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\', '
                        f'{input_audio_recording_options})')

        download_attempt = 1

        while download_attempt <= self._max_download_attempts:

            try:

                with YoutubeDL(self._get_downloader_options(user_id, input_audio_recording_options)) as downloader:

                    downloader.download([self._get_audio_recording_url(video_id)])

                audio_recording_file = self._get_audio_recording_file(user_id, input_audio_recording_options)
                audio_recording_file_megabytes = self._get_audio_recording_file_megabytes(user_id,
                                                                                          input_audio_recording_options)

                audio_recording = AudioRecording(id_=uuid4(),
                                                 video_id=video_id,
                                                 user_id=user_id,
                                                 title=input_audio_recording_options.title,
                                                 artist=input_audio_recording_options.artist,
                                                 file=audio_recording_file,
                                                 file_size_megabytes=audio_recording_file_megabytes,
                                                 codec=input_audio_recording_options.codec,
                                                 bit_rate=input_audio_recording_options.bit_rate)

                self._log.debug(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\', '
                                f'{input_audio_recording_options})')

                return audio_recording

            except Exception as exception:

                self._log.warning(f'Exception found while downloading audio recording on attempt {download_attempt}',
                                  extra={'exception': f'{exception.__class__.__name__}: {exception}'})

                download_attempt += 1

        else:

            raise AudioDownloadException

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

    def _get_downloader_options(self, user_id: UUID, input_audio_recording_options: InputAudioRecordingOptions) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': self._get_audio_recording_file_template(user_id, input_audio_recording_options),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': input_audio_recording_options.codec,
                    'preferredquality': str(input_audio_recording_options.bit_rate),
                },
                {
                    'key': 'EmbedThumbnail'
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={input_audio_recording_options.title}',
                '-metadata',
                f'artist={input_audio_recording_options.artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True,
            'writethumbnail': True
        }

        return options

    def _get_audio_recording_file_template(self, user_id: UUID,
                                           input_audio_recording_options: InputAudioRecordingOptions) -> str:

        user_audio_files_directory = self._audio_persistence.get_audio_files_directory_for_user(user_id)
        file_template = self._file_template.substitute(audio_recording_title=input_audio_recording_options.title,
                                                       audio_recording_artist=input_audio_recording_options.artist)

        return os.path.join(user_audio_files_directory, file_template)

    def _get_audio_recording_url(self, video_id: str) -> str:

        return self._url_template.substitute(video_id=video_id)

    def _get_audio_recording_file(self, user_id: UUID,
                                  input_audio_recording_options: InputAudioRecordingOptions) -> str:

        audio_recording_file_template = self._get_audio_recording_file_template(user_id, input_audio_recording_options)
        audio_recording_file = audio_recording_file_template % {'ext': input_audio_recording_options.codec}

        return audio_recording_file

    def _get_audio_recording_file_megabytes(self, user_id: UUID,
                                            input_audio_recording_options: InputAudioRecordingOptions) -> float:

        audio_recording_file = self._get_audio_recording_file(user_id, input_audio_recording_options)
        audio_recording_file_megabytes = os.stat(audio_recording_file).st_size / (1024 ** 2)

        return audio_recording_file_megabytes
