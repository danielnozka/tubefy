import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..adapters.music_adapter import MusicAdapter
from ..dtos.output_song import OutputSong
from ..exceptions.song_already_downloaded_exception import SongAlreadyDownloadedException
from ..exceptions.song_not_found_exception import SongNotFoundException
from .music_downloader import MusicDownloader
from ..persistence.music_persistence import MusicPersistence
from ..tools.typing import JsonType


class MusicService:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self,
                 music_adapter: MusicAdapter = Provide['music_adapter'],
                 music_downloader: MusicDownloader = Provide['music_downloader'],
                 music_persistence: MusicPersistence = Provide['music_persistence']):

        self._music_adapter = music_adapter
        self._music_downloader = music_downloader
        self._music_persistence = music_persistence

    def download_song(self, song_id: str, input_data: JsonType) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')
        song_exists = self._music_persistence.get_song_by_id(song_id) is not None

        if song_exists:

            raise SongAlreadyDownloadedException(song_id)

        else:

            input_song = self._music_adapter.adapt_input(song_id, input_data)
            song = self._music_downloader.download_song(input_song)
            database_song = self._music_adapter.adapt_to_persist(song)
            self._music_persistence.add_song(database_song)

        self._log.debug(f'End [funcName](song_id=\'{song_id}\')')

    def get_all_songs(self) -> list[OutputSong]:

        self._log.debug('Start [funcName]()')
        songs = self._music_persistence.get_all_songs()
        result = self._music_adapter.adapt_output(songs)
        self._log.debug('End [funcName]()')

        return result

    def delete_song(self, song_id: str) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')
        song = self._music_persistence.get_song_by_id(song_id)

        if song is not None:

            self._music_persistence.delete_song(song)

        else:

            raise SongNotFoundException(song_id)

        self._log.debug(f'End [funcName](song_id=\'{song_id}\')')
