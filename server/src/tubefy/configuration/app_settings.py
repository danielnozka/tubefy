import json
import os

from .persistence_settings import PersistenceSettings
from .server_settings import ServerSettings


class AppSettings:

    def __init__(self, root_path: str, settings_file: str):

        self.root_path = root_path
        settings = self._open_config_file(settings_file)
        audio_database_directory = self._get_absolute_path(settings['persistenceSettings']['audioDatabaseDirectory'])
        audio_files_directory = self._get_absolute_path(settings['persistenceSettings']['audioFilesDirectory'])
        host = settings['serverSettings']['host']
        port = settings['serverSettings']['port']
        self.persistence_settings = PersistenceSettings(audio_database_directory, audio_files_directory)
        self.server_settings = ServerSettings(host, port)

    @staticmethod
    def _open_config_file(settings_file: str) -> dict:

        with open(settings_file, 'r') as file:

            settings = json.load(file)

        return settings

    def _get_absolute_path(self, path: str) -> str:

        if os.path.isabs(path):

            return os.path.normpath(path)

        else:

            return os.path.normpath(os.path.join(self.root_path, path))
