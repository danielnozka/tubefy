import json
import logging
import logging.config

from dependency_injector.wiring import inject, Provide
from pathlib import Path

from ..configuration import AppSettings
from .directory_handler import DirectoryHandler


class LoggingHandler:

    _handlers_key: str = 'handlers'
    _handler_filename_key: str = 'filename'
    _settings: dict
    _data_path: Path
    _directory_handler: DirectoryHandler

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_handler: DirectoryHandler = Provide['directory_handler']
    ):

        self._settings = app_settings.logging_settings
        self._data_path = directory_handler.create_directory(app_settings.persistence_settings.data_path)
        self._directory_handler = directory_handler

    def build(self) -> None:

        self._setup_file_handlers()
        logging.config.dictConfig(self._settings)

    @staticmethod
    def close() -> None:

        logging.getLogger().handlers.clear()

    @staticmethod
    def _open_file(file_path: Path) -> dict:

        with open(file_path, 'r') as file:

            result = json.load(file)

        return result

    def _setup_file_handlers(self) -> None:

        for handler_name, handler_options in self._settings[self._handlers_key].items():

            if self._is_file_handler(handler_options):

                file_handler_file_path = self._data_path.joinpath(handler_options[self._handler_filename_key])
                self._update_file_handler_path(handler_name, file_handler_file_path)

    def _is_file_handler(self, handler_options: dict) -> bool:

        return self._handler_filename_key in handler_options

    def _update_file_handler_path(self, handler_name: str, handler_path: Path) -> None:

        self._settings[self._handlers_key][handler_name][self._handler_filename_key] = handler_path
