import os
import sqlite3

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from sqlite3 import Connection

from ..configuration.app_settings import AppSettings
from .domain.database_song import DatabaseSong
from ..exceptions.database_connection_exception import DatabaseConnectionException
from ..exceptions.database_query_exception import DatabaseQueryException


class MusicContext:

    _database_file = 'music.db'
    _songs_table = 'songs'
    _songs_column_id = 'id'
    _songs_column_title = 'title'
    _songs_column_artist = 'artist'
    _songs_column_creation_date = 'creation_date'
    _songs_column_file = 'file'

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._music_database_directory = os.path.abspath(app_settings.persistence_settings.music_database_directory)
        self._database = os.path.join(self._music_database_directory, self._database_file)

        if not os.path.isfile(self._database):

            self._create_database()

    def add_song(self, song: DatabaseSong) -> None:

        query = (f'INSERT INTO {self._songs_table}({self._songs_column_id}, {self._songs_column_title}, '
                 f'{self._songs_column_artist}, {self._songs_column_creation_date}, {self._songs_column_file}) '
                 f'VALUES("{song.id}", "{song.title}", "{song.artist}", "{song.creation_date}", "{song.file}")')

        self._make_query(query)

    def get_all(self) -> list[DatabaseSong]:

        query = f'SELECT * FROM {self._songs_table}'
        query_result = self._make_query(query)
        result = [DatabaseSong(*element) for element in query_result]
        return result

    def delete(self, song: DatabaseSong) -> None:

        query = f'DELETE FROM {self._songs_table} WHERE {self._songs_column_id}="{song.id}"'
        self._make_query(query)

    def _create_database(self) -> None:

        if not self._database_directory_exists():

            self._create_database_directory()

        query = (f'CREATE TABLE {self._songs_table} '
                 f'({self._songs_column_id} TEXT NOT NULL PRIMARY KEY, '
                 f'{self._songs_column_title} TEXT NOT NULL, '
                 f'{self._songs_column_artist} TEXT NOT NULL, '
                 f'{self._songs_column_creation_date} TEXT NOT NULL, '
                 f'{self._songs_column_file} TEXT NOT NULL)')

        self._make_query(query)

    def _database_directory_exists(self) -> bool:

        return os.path.isdir(self._music_database_directory)

    def _create_database_directory(self) -> None:

        os.makedirs(self._music_database_directory, exist_ok=True)

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
