import json
import logging
import logging.config

from dependency_injector.wiring import inject, Provide
from pathlib import Path

from .directory_builder import DirectoryBuilder


class LoggingBuilder:

    _settings_file: str = 'log_settings.json'
    _handlers_key: str = 'handlers'
    _handler_filename_key: str = 'filename'
    _root_path: Path
    _directory_builder: DirectoryBuilder
    _settings: dict

    @inject
    def __init__(
        self,
        root_path: Path,
        directory_builder: DirectoryBuilder = Provide['directory_builder']
    ):

        self._root_path = root_path
        self._directory_builder = directory_builder

    def build(self) -> None:

        self._open_settings_file()
        self._setup_file_handlers()
        logging.config.dictConfig(self._settings)

    def _open_settings_file(self) -> None:

        with open(self._root_path.joinpath(self._settings_file), 'r') as file:

            self._settings = json.load(file)

    def _setup_file_handlers(self) -> None:

        for handler_name, handler_options in self._settings[self._handlers_key].items():

            if self._is_file_handler(handler_options):

                file_handler_path = Path(handler_options[self._handler_filename_key])
                file_handler_directory = self._directory_builder.build(file_handler_path.parent)
                file_handler_filename = file_handler_path.name
                self._update_file_handler_path(handler_name, file_handler_directory.joinpath(file_handler_filename))

    def _is_file_handler(self, handler_options: dict) -> bool:

        return self._handler_filename_key in handler_options

    def _update_file_handler_path(self, handler_name: str, handler_path: Path) -> None:

        self._settings[self._handlers_key][handler_name][self._handler_filename_key] = handler_path
