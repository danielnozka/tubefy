import json

from pathlib import Path

from .audio_conversion_settings import AudioConversionSettings
from .persistence_settings import PersistenceSettings
from .server_settings import ServerSettings


class AppSettings:

    audio_conversion_settings: AudioConversionSettings
    persistence_settings: PersistenceSettings
    server_settings: ServerSettings
    _settings_file: str = 'app_settings.json'
    _root_path: Path
    _settings: dict

    def __init__(self, root_path: Path):

        self._root_path = root_path
        self._open_settings_file()
        self.audio_conversion_settings = AudioConversionSettings(**self._settings['audio_conversion_settings'])
        self.persistence_settings = PersistenceSettings(**self._settings['persistence_settings'])
        self.server_settings = ServerSettings(**self._settings['server_settings'])

    def _open_settings_file(self) -> None:

        with open(self._root_path.joinpath(self._settings_file), 'r') as file:

            self._settings = json.load(file)
