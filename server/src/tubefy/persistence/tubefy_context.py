import os
import sqlite3

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from sqlite3 import Connection
from uuid import UUID

from ..configuration.app_settings import AppSettings
from ..domain.audio_recording import AudioRecording
from ..domain.user import User
from ..exceptions.database_connection_exception import DatabaseConnectionException
from ..exceptions.database_query_exception import DatabaseQueryException


class TubefyContext:

    class _UsersTable:

        table_name: str = 'users'
        id_column: str = 'id'
        username_column: str = 'username'
        token_column: str = 'token'

    class _AudioRecordingsTable:

        table_name: str = 'audio_recordings'
        id_column: str = 'id'
        video_id_column: str = 'video_id'
        user_id_column: str = 'user_id'
        title_column: str = 'title'
        artist_column: str = 'artist'
        file_column: str = 'file'
        file_size_megabytes_column: str = 'file_size_megabytes'
        codec_column: str = 'codec'
        bit_rate_column: str = 'bit_rate'

    _database_file: str = 'tubefy.db'
    _audio_database_directory: str
    _database: str

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._audio_database_directory = os.path.abspath(app_settings.persistence_settings.audio_database_directory)
        self._database = os.path.join(self._audio_database_directory, self._database_file)

        if not self._database_file_exists():

            self._create_database()

    def get_user_by_username(self, username: str) -> User | None:

        query = f'SELECT * FROM {self._UsersTable.table_name} WHERE {self._UsersTable.username_column}="{username}"'
        query_result = self._make_query(query)

        if self._query_result_is_empty(query_result):

            return None

        else:

            return User(*query_result[0])

    def register_user(self, user: User) -> None:

        query = (f'INSERT INTO {self._UsersTable.table_name}({self._UsersTable.id_column}, '
                 f'{self._UsersTable.username_column}, {self._UsersTable.token_column}) '
                 f'VALUES("{user.id}", "{user.username}", "{user.token}")')

        self._make_query(query)

    def save_user_audio_recording(self, audio_recording: AudioRecording) -> None:

        query = (f'INSERT INTO {self._AudioRecordingsTable.table_name}({self._AudioRecordingsTable.id_column}, '
                 f'{self._AudioRecordingsTable.video_id_column}, {self._AudioRecordingsTable.user_id_column}, '
                 f'{self._AudioRecordingsTable.title_column}, {self._AudioRecordingsTable.artist_column}, '
                 f'{self._AudioRecordingsTable.file_column}, {self._AudioRecordingsTable.file_size_megabytes_column}, '
                 f'{self._AudioRecordingsTable.codec_column}, {self._AudioRecordingsTable.bit_rate_column}) '
                 f'VALUES("{audio_recording.id}", "{audio_recording.video_id}", "{audio_recording.user_id}", '
                 f'"{audio_recording.title}", "{audio_recording.artist}", "{audio_recording.file}", '
                 f'"{audio_recording.file_size_megabytes}", "{audio_recording.codec}", "{audio_recording.bit_rate}")')

        self._make_query(query)

    def get_all_user_audio_recordings(self, user_id: UUID) -> list[AudioRecording]:

        query = (f'SELECT * FROM {self._AudioRecordingsTable.table_name} '
                 f'WHERE {self._AudioRecordingsTable.user_id_column}="{user_id}"')
        query_result = self._make_query(query)
        result = [AudioRecording(*element) for element in query_result]

        return result

    def get_user_audio_recording_by_video_id(self, user_id: UUID, video_id: str) -> AudioRecording | None:

        query = (f'SELECT * FROM {self._AudioRecordingsTable.table_name} '
                 f'WHERE {self._AudioRecordingsTable.user_id_column}="{user_id}" '
                 f'AND {self._AudioRecordingsTable.video_id_column}="{video_id}"')
        query_result = self._make_query(query)

        if self._query_result_is_empty(query_result):

            return None

        else:

            return AudioRecording(*query_result[0])

    def get_audio_recording_by_recording_id(self, recording_id: UUID) -> AudioRecording | None:

        query = (f'SELECT * FROM {self._AudioRecordingsTable.table_name} '
                 f'WHERE {self._AudioRecordingsTable.id_column}="{recording_id}"')
        query_result = self._make_query(query)

        if self._query_result_is_empty(query_result):

            return None

        else:

            return AudioRecording(*query_result[0])

    def delete_user_audio_recording(self, audio_recording: AudioRecording) -> None:

        query = (f'DELETE FROM {self._AudioRecordingsTable.table_name} '
                 f'WHERE {self._AudioRecordingsTable.id_column}="{audio_recording.id}"')
        self._make_query(query)

    def _database_file_exists(self) -> bool:

        return os.path.isfile(self._database)

    def _create_database(self) -> None:

        if not self._database_directory_exists():

            self._create_database_directory()

        users_query = (f'CREATE TABLE {self._UsersTable.table_name} '
                       f'({self._UsersTable.id_column} TEXT NOT NULL PRIMARY KEY, '
                       f'{self._UsersTable.username_column} TEXT NOT NULL, '
                       f'{self._UsersTable.token_column} TEXT NOT NULL)')

        self._make_query(users_query)

        audio_recordings_query = (f'CREATE TABLE {self._AudioRecordingsTable.table_name} '
                                  f'({self._AudioRecordingsTable.id_column} TEXT NOT NULL PRIMARY KEY, '
                                  f'{self._AudioRecordingsTable.video_id_column} TEXT NOT NULL, '
                                  f'{self._AudioRecordingsTable.user_id_column} TEXT NOT NULL, '
                                  f'{self._AudioRecordingsTable.title_column} TEXT NOT NULL, '
                                  f'{self._AudioRecordingsTable.artist_column} TEXT NOT NULL, '
                                  f'{self._AudioRecordingsTable.file_column} TEXT NOT NULL,'
                                  f'{self._AudioRecordingsTable.file_size_megabytes_column} REAL NOT NULL,'
                                  f'{self._AudioRecordingsTable.codec_column} TEXT NOT NULL,'
                                  f'{self._AudioRecordingsTable.bit_rate_column} INTEGER NOT NULL)')

        self._make_query(audio_recordings_query)

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
