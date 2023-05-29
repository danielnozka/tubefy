import os
import sqlite3

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from sqlite3 import Connection

from ..configuration.app_settings import AppSettings
from ..domain.audio_recording import AudioRecording
from ..exceptions.database_connection_exception import DatabaseConnectionException
from ..exceptions.database_query_exception import DatabaseQueryException


class AudioContext:

    _database_file = 'audio.db'

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._audio_table = self.AudioTable()
        self._audio_database_directory = os.path.abspath(app_settings.persistence_settings.audio_database_directory)
        self._database = os.path.join(self._audio_database_directory, self._database_file)

        if not self._database_file_exists():

            self._create_database()

    def add_audio_recording(self, audio_recording: AudioRecording) -> None:

        query = (f'INSERT INTO {self._audio_table.name}({self._audio_table.id_column}, '
                 f'{self._audio_table.title_column}, {self._audio_table.artist_column}, '
                 f'{self._audio_table.file_column}, {self._audio_table.file_size_megabytes_column}, '
                 f'{self._audio_table.codec_column}, {self._audio_table.bit_rate_column}) '
                 f'VALUES("{audio_recording.id}", "{audio_recording.title}", "{audio_recording.artist}", '
                 f'"{audio_recording.file}", "{audio_recording.file_size_megabytes}", "{audio_recording.codec}", '
                 f'"{audio_recording.bit_rate}")')

        self._make_query(query)

    def get_all_audio_recordings(self) -> list[AudioRecording]:

        query = f'SELECT * FROM {self._audio_table.name}'
        query_result = self._make_query(query)
        result = [AudioRecording(*element) for element in query_result]

        return result

    def get_audio_recording_by_id(self, audio_id: str) -> AudioRecording | None:

        query = f'SELECT * FROM {self._audio_table.name} WHERE {self._audio_table.id_column}="{audio_id}"'
        query_result = self._make_query(query)

        if self._query_result_is_empty(query_result):

            return None

        else:

            return AudioRecording(*query_result[0])

    def delete_audio_recording(self, audio_recording: AudioRecording) -> None:

        query = f'DELETE FROM {self._audio_table.name} WHERE {self._audio_table.id_column}="{audio_recording.id}"'
        self._make_query(query)

    def _database_file_exists(self) -> bool:

        return os.path.isfile(self._database)

    def _create_database(self) -> None:

        if not self._database_directory_exists():

            self._create_database_directory()

        query = (f'CREATE TABLE {self._audio_table.name} '
                 f'({self._audio_table.id_column} TEXT NOT NULL PRIMARY KEY, '
                 f'{self._audio_table.title_column} TEXT NOT NULL, '
                 f'{self._audio_table.artist_column} TEXT NOT NULL, '
                 f'{self._audio_table.file_column} TEXT NOT NULL,'
                 f'{self._audio_table.file_size_megabytes_column} REAL NOT NULL,'
                 f'{self._audio_table.codec_column} TEXT NOT NULL,'
                 f'{self._audio_table.bit_rate_column} INTEGER NOT NULL)')

        self._make_query(query)

    def _database_directory_exists(self) -> bool:

        return os.path.isdir(self._audio_database_directory)

    def _create_database_directory(self) -> None:

        os.makedirs(self._audio_database_directory, exist_ok=True)

    def _make_query(self, query: str) -> list[tuple]:

        connection = self._connect()

        try:

            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()

            return result

        except Exception as exception:

            raise DatabaseQueryException(exception)

    def _connect(self) -> Connection:

        try:

            connection = sqlite3.connect(self._database)
            return connection

        except Exception as exception:

            raise DatabaseConnectionException(exception)

    @staticmethod
    def _query_result_is_empty(query_result: list[tuple]) -> bool:

        return len(query_result) == 0

    class AudioTable:

        name = 'songs'
        id_column = 'id'
        title_column = 'title'
        artist_column = 'artist'
        file_column = 'file'
        file_size_megabytes_column = 'file_size_megabytes'
        codec_column = 'codec'
        bit_rate_column = 'bit_rate'
