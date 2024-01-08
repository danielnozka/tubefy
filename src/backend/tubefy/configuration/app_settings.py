import json

from pathlib import Path

from .audio_conversion_settings import AudioConversionSettings
from .persistence_settings import PersistenceSettings
from .security_settings import SecuritySettings
from .server_settings import ServerSettings


class AppSettings:

    audio_conversion_settings: AudioConversionSettings
    logging_settings: dict
    persistence_settings: PersistenceSettings
    security_settings: SecuritySettings
    server_settings: ServerSettings

    def __init__(self, settings_file_path: Path):

        settings: dict = self._open_file(settings_file_path)
        self.audio_conversion_settings = AudioConversionSettings(**settings['audio_conversion_settings'])
        self.logging_settings = settings['logging_settings']
        self.persistence_settings = PersistenceSettings(**settings['persistence_settings'])
        self.security_settings = SecuritySettings(**settings['security_settings'])
        self.server_settings = ServerSettings(**settings['server_settings'])

    @staticmethod
    def _open_file(file_path: Path) -> dict:

        with open(file_path, 'r') as file:

            result = json.load(file)

        return result
