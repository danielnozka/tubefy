import logging
import os
import platform
import py7zr

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from ..exceptions.audio_download_exception import AudioDownloadException
from string import Template
from youtube_dl import YoutubeDL

from ..domain.audio_recording import AudioRecording
from ..dtos.input_audio_recording import InputAudioRecording
from ..persistence.audio_persistence import AudioPersistence


class AudioDownloader:

    _log = logging.getLogger(__name__)
    _url_template = Template('https://www.youtube.com/watch?v=${audio_recording_id}')
    _current_directory = os.path.dirname(__file__)
    _ffmpeg_windows_binary_files = os.path.join(_current_directory, 'ffmpeg.7z')
    _ffmpeg_linux_path = '/usr/bin/ffmpeg'
    _max_download_attempts = 3

    @inject
    def __init__(self, audio_persistence: AudioPersistence = Provide['audio_persistence']):

        self._audio_persistence = audio_persistence
        self._ffmpeg_location = self._get_ffmpeg_location()
        self._file_template = Template(os.path.join(self._audio_persistence.get_audio_files_directory(),
                                                    '${audio_recording_artist} - ${audio_recording_title}.%(ext)s'))

    def download_audio_recording(self, input_audio_recording: InputAudioRecording) -> AudioRecording:

        self._log.debug(f'Start [funcName]({input_audio_recording})')

        download_attempt = 0

        while download_attempt < self._max_download_attempts:

            try:

                with YoutubeDL(self._get_downloader_options(input_audio_recording)) as downloader:

                    downloader.download([self._get_audio_recording_url(input_audio_recording)])

                audio_recording_file = self._get_audio_recording_file(input_audio_recording)
                audio_recording_file_megabytes = self._get_audio_recording_file_megabytes(input_audio_recording)

                audio_recording = AudioRecording(id_=input_audio_recording.id,
                                                 title=input_audio_recording.title,
                                                 artist=input_audio_recording.artist,
                                                 file=audio_recording_file,
                                                 file_size_megabytes=audio_recording_file_megabytes,
                                                 codec=input_audio_recording.codec,
                                                 bit_rate=input_audio_recording.bit_rate)

                self._log.debug(f'End [funcName]({input_audio_recording})')

                return audio_recording

            except Exception as exception:

                self._log.warning(f'Exception found while downloading audio recording on attempt '
                                  f'{download_attempt + 1}',
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

    def _get_downloader_options(self, input_audio_recording: InputAudioRecording) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': self._get_audio_recording_file_template(input_audio_recording),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': input_audio_recording.codec,
                    'preferredquality': str(input_audio_recording.bit_rate),
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={input_audio_recording.title}',
                '-metadata',
                f'artist={input_audio_recording.artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        return options

    def _get_audio_recording_file_template(self, input_audio_recording: InputAudioRecording) -> str:

        return self._file_template.substitute(audio_recording_title=input_audio_recording.title,
                                              audio_recording_artist=input_audio_recording.artist)

    def _get_audio_recording_url(self, input_audio_recording: InputAudioRecording) -> str:

        return self._url_template.substitute(audio_recording_id=input_audio_recording.id)

    def _get_audio_recording_file(self, input_audio_recording: InputAudioRecording) -> str:

        audio_recording_file_template = self._get_audio_recording_file_template(input_audio_recording)
        audio_recording_file = audio_recording_file_template % {'ext': input_audio_recording.codec}

        return audio_recording_file

    def _get_audio_recording_file_megabytes(self, input_audio_recording: InputAudioRecording) -> float:

        audio_recording_file = self._get_audio_recording_file(input_audio_recording)
        audio_recording_file_megabytes = os.stat(audio_recording_file).st_size / (1024 ** 2)

        return audio_recording_file_megabytes
