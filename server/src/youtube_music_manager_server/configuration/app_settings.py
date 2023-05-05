import json
import os.path

from .persistence_settings import PersistenceSettings
from .server_settings import ServerSettings


class AppSettings:

    def __init__(self, root_path: str, settings_file: str):

        settings = self._open_config_file(settings_file)
        music_database_path = self._get_absolute_path(root_path, settings['persistenceSettings']['musicDatabasePath'])
        music_files_directory = \
            self._get_absolute_path(root_path, settings['persistenceSettings']['musicFilesDirectory'])
        host = settings['serverSettings']['host']
        port = settings['serverSettings']['port']

        self.root_path = root_path
        self.persistence_settings = PersistenceSettings(music_database_path, music_files_directory)
        self.server_settings = ServerSettings(host, port)

    @staticmethod
    def _open_config_file(settings_file: str) -> dict:

        with open(settings_file, 'r') as file:

            settings = json.load(file)

        return settings

    @staticmethod
    def _get_absolute_path(root_path: str, path: str) -> str:

        if not os.path.isabs(path):

            return os.path.normpath(os.path.join(root_path, path))
