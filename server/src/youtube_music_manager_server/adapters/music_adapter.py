import logging

from ..domain.song import Song
from ..dtos.input_song import InputSong
from ..dtos.output_song import OutputSong
from ..persistence.domain.database_song import DatabaseSong
from ..tools.typing import JsonType


class MusicAdapter:

    _log = logging.getLogger(__name__)
    _datetime_format = '%d-%m-%Y %H:%M:%S.%f'

    def adapt_input(self, song_id: str, input_data: JsonType) -> InputSong:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')

        input_song = InputSong(id_=song_id,
                               title=input_data['title'],
                               artist=input_data['artist'],
                               audio_codec=input_data['audioCodec'].lower(),
                               audio_bit_rate=int(input_data['audioBitRate']))

        self._log.debug(f'End [funcName](song_id=\'{song_id}\')')

        return input_song

    def adapt_to_persist(self, song: Song) -> DatabaseSong:

        self._log.debug(f'Start [funcName](song_id=\'{song.id}\')')

        database_song = DatabaseSong(id_=song.id,
                                     title=song.title,
                                     artist=song.artist,
                                     creation_date=song.creation_date.strftime(self._datetime_format),
                                     file=song.file,
                                     file_size_megabytes=song.file_size_megabytes,
                                     audio_codec=song.audio_codec,
                                     audio_bit_rate=song.audio_bit_rate)

        self._log.debug(f'End [funcName](song_id=\'{song.id}\')')

        return database_song

    def adapt_output(self, songs: list[DatabaseSong]) -> list[OutputSong]:

        self._log.debug('Start [funcName]()')

        result = []

        for song in songs:

            output_song = OutputSong(id_=song.id,
                                     title=song.title,
                                     artist=song.artist,
                                     file_size_megabytes=song.file_size_megabytes,
                                     audio_codec=song.audio_codec.upper(),
                                     audio_bit_rate=song.audio_bit_rate)

            result.append(output_song)

        self._log.debug('End [funcName]()')

        return result
