import logging
import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..configuration.app_settings import AppSettings
from .domain.database_song import DatabaseSong
from ..exceptions.song_file_not_found_exception import SongFileNotFoundException
from .music_context import MusicContext


class MusicPersistence:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._context = MusicContext()
        self._music_files_directory = os.path.abspath(app_settings.persistence_settings.music_files_directory)

        if not self._music_files_directory_exists():

            self._create_music_files_directory()

    def get_music_files_directory(self) -> str:

        return self._music_files_directory

    def add_song(self, song: DatabaseSong) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song.id}\')')
        self._context.add_song(song)
        self._log.debug(f'End [funcName](song_id=\'{song.id}\')')

    def get_all_songs(self) -> list[DatabaseSong]:

        self._log.debug(f'Start [funcName]()')
        result = self._context.get_all_songs()
        self._log.debug(f'End [funcName]()')

        return result

    def get_song_by_id(self, song_id: str) -> DatabaseSong | None:

        self._log.debug(f'Start [funcName]()')
        result = self._context.get_song_by_id(song_id)
        self._log.debug(f'End [funcName]()')

        return result

    def delete_song(self, song: DatabaseSong) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song.id}\')')
        self._context.delete_song(song)
        self._delete_song_file(song)
        self._log.debug(f'End [funcName](song_id=\'{song.id}\')')

    def _music_files_directory_exists(self) -> bool:

        return os.path.isdir(self._music_files_directory)

    def _create_music_files_directory(self) -> None:

        os.makedirs(self._music_files_directory, exist_ok=True)

    @staticmethod
    def _delete_song_file(song: DatabaseSong) -> None:

        if os.path.isfile(song.file):

            os.remove(song.file)

        else:

            raise SongFileNotFoundException(song.file)
