import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..domain.song import Song
from ..dtos.song_dto import SongDto
from .json_adapter import JsonAdapter
from ..persistence.domain.database_song import DatabaseSong
from ..tools.typing import JsonType


class MusicAdapter:

    _log = logging.getLogger(__name__)
    _datetime_format = '%d-%m-%Y %H:%M:%S.%f'

    @inject
    def __init__(self, json_adapter: JsonAdapter = Provide['json_adapter']):

        self._json_adapter = json_adapter

    def adapt_input(self, song_id: str, input_data: JsonType) -> SongDto:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')
        song = SongDto(id_=song_id, title=input_data['title'], artist=input_data['artist'])
        self._log.debug(f'End [funcName](song_id=\'{song_id}\')')

        return song

    def adapt_to_persist(self, song: Song) -> DatabaseSong:

        self._log.debug(f'Start [funcName](song_id=\'{song.id}\')')

        database_song = DatabaseSong(id_=song.id,
                                     title=song.title,
                                     artist=song.artist,
                                     creation_date=song.creation_date.strftime(self._datetime_format),
                                     file=song.file)

        self._log.debug(f'End [funcName](song_id=\'{song.id}\')')

        return database_song

    def adapt_output(self, songs: list[DatabaseSong]) -> JsonType:

        self._log.debug('Start [funcName]()')

        result = []

        for song in songs:

            song_dto = SongDto(id_=song.id, title=song.title, artist=song.artist)
            song_output = self._json_adapter.adapt(song_dto)
            result.append(song_output)

        self._log.debug('End [funcName]()')

        return result
