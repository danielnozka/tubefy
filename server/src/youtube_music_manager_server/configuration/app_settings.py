import json
import os

from .music_downloader_settings import MusicDownloaderSettings
from .persistence_settings import PersistenceSettings
from .server_settings import ServerSettings


class AppSettings:

    def __init__(self, root_path: str, settings_file: str):

        settings = self._open_config_file(settings_file)
        audio_codec = settings['musicDownloaderSettings']['audioCodec']
        audio_bit_rate = settings['musicDownloaderSettings']['audioBitRate']
        music_database_directory = os.path.normpath(settings['persistenceSettings']['musicDatabaseDirectory'])
        music_files_directory = os.path.normpath(settings['persistenceSettings']['musicFilesDirectory'])
        host = settings['serverSettings']['host']
        port = settings['serverSettings']['port']

        self.root_path = root_path
        self.music_downloader_settings = MusicDownloaderSettings(audio_codec, audio_bit_rate)
        self.persistence_settings = PersistenceSettings(music_database_directory, music_files_directory)
        self.server_settings = ServerSettings(host, port)

    @staticmethod
    def _open_config_file(settings_file: str) -> dict:

        with open(settings_file, 'r') as file:

            settings = json.load(file)

        return settings