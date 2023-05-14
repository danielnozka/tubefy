import logging

from .domain.database_song import DatabaseSong
from .music_context import MusicContext


class MusicPersistence:

    _log = logging.getLogger(__name__)

    def __init__(self):

        self._context = MusicContext()

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
        self._log.debug(f'End [funcName](song_id=\'{song.id}\')')
