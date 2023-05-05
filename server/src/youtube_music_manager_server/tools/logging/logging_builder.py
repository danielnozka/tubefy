import json
import logging
import logging.config
import os

from typing_extensions import Self


class LoggingBuilder:

    _config_handlers_key = 'handlers'
    _handler_filename_key = 'filename'

    def __init__(self):

        pass

    def configure(self, config_file: str) -> Self:

        config = self._open_config_file(config_file)
        self._create_file_handlers_directories(config[self._config_handlers_key])
        logging.config.dictConfig(config)

        return self

    @staticmethod
    def _open_config_file(config_file: str) -> dict:

        with open(config_file, 'r') as file:

            config = json.load(file)

        return config

    def _create_file_handlers_directories(self, handlers: dict) -> None:

        for handler in handlers.values():

            if self._is_file_handler(handler):

                file_handler_directory = os.path.dirname(os.path.normpath(handler[self._handler_filename_key]))
                os.makedirs(file_handler_directory, exist_ok=True)

    def _is_file_handler(self, handler: dict) -> bool:

        return self._handler_filename_key in handler
