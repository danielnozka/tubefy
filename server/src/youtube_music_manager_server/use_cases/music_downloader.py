import logging
import os
import platform
import py7zr

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from string import Template
from youtube_dl import YoutubeDL

from ..configuration.app_settings import AppSettings
from ..domain.song import Song
from ..dtos.song_dto import SongDto
from ..persistence.music_persistence import MusicPersistence


class MusicDownloader:

    _log = logging.getLogger(__name__)
    _url_template = Template('https://www.youtube.com/watch?v=${song_id}')
    _current_directory = os.path.dirname(__file__)
    _ffmpeg_windows_binary_files = os.path.join(_current_directory, 'ffmpeg.7z')
    _ffmpeg_linux_path = '/usr/bin/ffmpeg'

    @inject
    def __init__(self,
                 app_settings: AppSettings = Provide['app_settings'],
                 music_persistence: MusicPersistence = Provide['music_persistence']):

        self._codec = app_settings.music_downloader_settings.audio_codec
        self._bit_rate = app_settings.music_downloader_settings.audio_bit_rate
        self._music_persistence = music_persistence
        self._ffmpeg_location = self._get_ffmpeg_location()
        self._file_template = Template(os.path.join(self._music_persistence.get_music_files_directory(),
                                                    '${song_artist} - ${song_title}.%(ext)s'))

    def download_song(self, input_song: SongDto) -> Song:

        self._log.debug(f'Start [funcName](song_id=\'{input_song.id}\')')

        with YoutubeDL(self._get_downloader_options(input_song.title, input_song.artist)) as downloader:

            downloader.download([self._get_song_url(input_song.id)])

        song = Song(id_=input_song.id,
                    title=input_song.title,
                    artist=input_song.artist,
                    creation_date=datetime.now(),
                    file=self._get_song_mp3_file(input_song.title, input_song.artist))

        self._log.debug(f'End [funcName](song_id=\'{input_song.id}\')')

        return song

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

    def _get_downloader_options(self, song_title: str, song_artist: str) -> dict:

        options = {
            'ffmpeg_location': self._ffmpeg_location,
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': self._get_song_file_template(song_title, song_artist),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self._codec,
                    'preferredquality': self._bit_rate,
                }
            ],
            'postprocessor_args': [
                '-metadata',
                f'title={song_title}',
                '-metadata',
                f'artist={song_artist}'
            ],
            'prefer_ffmpeg': True,
            'quiet': True
        }

        return options

    def _get_song_file_template(self, song_title: str, song_artist: str) -> str:

        return self._file_template.substitute(song_title=song_title, song_artist=song_artist)

    def _get_song_mp3_file(self, song_title: str, song_artist: str) -> str:

        song_file_template = self._get_song_file_template(song_title, song_artist)
        song_mp3_file = song_file_template % {'ext': self._codec}

        return song_mp3_file

    def _get_song_url(self, song_id: str) -> str:

        return self._url_template.substitute(song_id=song_id)
