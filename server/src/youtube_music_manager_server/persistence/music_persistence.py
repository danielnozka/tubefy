import logging

from .domain.database_song import DatabaseSong
from .music_context import MusicContext


class MusicPersistence:

    _log = logging.getLogger(__name__)

    def __init__(self):

        self._context = MusicContext()

    def add_song(self, song: DatabaseSong) -> None:

        self._log.debug(f'Start [funcName](id=\'{song.id}\')')
        self._context.add_song(song)
        self._log.debug(f'End [funcName](id=\'{song.id}\')')

    def get_all(self) -> list[DatabaseSong]:

        self._log.debug(f'Start [funcName]()')
        result = self._context.get_all()
        self._log.debug(f'End [funcName]()')
        return result

    def delete(self, song: DatabaseSong) -> None:

        self._log.debug(f'Start [funcName](id=\'{song.id}\')')
        self._context.delete(song)
        self._log.debug(f'End [funcName](id=\'{song.id}\')')
