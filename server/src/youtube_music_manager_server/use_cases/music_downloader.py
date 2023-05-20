import logging
import os
import platform
import py7zr

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from ..exceptions.song_download_exception import SongDownloadException
from string import Template
from youtube_dl import YoutubeDL

from ..domain.song import Song
from ..dtos.input_song import InputSong
from ..persistence.music_persistence import MusicPersistence


class MusicDownloader:

    _log = logging.getLogger(__name__)
    _url_template = Template('https://www.youtube.com/watch?v=${song_id}')
    _current_directory = os.path.dirname(__file__)
    _ffmpeg_windows_binary_files = os.path.join(_current_directory, 'ffmpeg.7z')
    _ffmpeg_linux_path = '/usr/bin/ffmpeg'
    _max_download_attempts = 3

    @inject
    def __init__(self, music_persistence: MusicPersistence = Provide['music_persistence']):

        self._music_persistence = music_persistence
        self._ffmpeg_location = self._get_ffmpeg_location()
        self._file_template = Template(os.path.join(self._music_persistence.get_music_files_directory(),
                                                    '${song_artist} - ${song_title}.%(ext)s'))

    def download_song(self, input_song: InputSong) -> Song:

        self._log.debug(f'Start [funcName](song_id=\'{input_song.id}\')')

        download_attempt = 0

        while download_attempt < self._max_download_attempts:

            try:

                with YoutubeDL(self._get_downloader_options(input_song)) as downloader:

                    downloader.download([self._get_song_url(input_song)])

                song = Song(id_=input_song.id,
                            title=input_song.title,
                            artist=input_song.artist,
                            creation_date=datetime.now(),
                            file=self._get_song_mp3_file(input_song),
                            file_size_megabytes=self._get_song_mp3_file_megabytes(input_song),
                            audio_codec=input_song.audio_codec,
                            audio_bit_rate=input_song.audio_bit_rate)

                self._log.debug(f'End [funcName](song_id=\'{input_song.id}\')')

                return song

            except Exception as exception:

                self._log.warning(f'Exception found while downloading song on attempt {download_attempt + 1}',
                                  extra={'exception': f'{exception.__class__.__name__}: {exception}'})

                download_attempt += 1

        else:

            raise SongDownloadException

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

    def _get_downloader_options(self, input_song: InputSong) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': self._get_song_file_template(input_song),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': input_song.audio_codec,
                    'preferredquality': str(input_song.audio_bit_rate),
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={input_song.title}',
                '-metadata',
                f'artist={input_song.artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        return options

    def _get_song_file_template(self, input_song: InputSong) -> str:

        return self._file_template.substitute(song_title=input_song.title, song_artist=input_song.artist)

    def _get_song_url(self, input_song: InputSong) -> str:

        return self._url_template.substitute(song_id=input_song.id)

    def _get_song_mp3_file(self, input_song: InputSong) -> str:

        song_file_template = self._get_song_file_template(input_song)
        song_mp3_file = song_file_template % {'ext': input_song.audio_codec}

        return song_mp3_file

    def _get_song_mp3_file_megabytes(self, input_song: InputSong) -> float:

        song_mp3_file = self._get_song_mp3_file(input_song)
        song_mp3_file_megabytes = os.stat(song_mp3_file).st_size / (1024 ** 2)

        return song_mp3_file_megabytes
