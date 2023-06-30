import json
import logging
import logging.config
import os


class LoggingBuilder:

    _config_handlers_key: str = 'handlers'
    _handler_filename_key: str = 'filename'
    _root_path: str
    _config: dict

    def __init__(self, root_path: str, config_file: str):

        self._root_path = root_path
        self._config = self._open_config_file(config_file)

    def configure(self) -> None:

        self._configure_file_handlers()
        logging.config.dictConfig(self._config)

    @staticmethod
    def _open_config_file(config_file: str) -> dict:

        with open(config_file, 'r') as file:

            config = json.load(file)

        return config

    def _configure_file_handlers(self) -> None:

        for handler_name, handler_options in self._config[self._config_handlers_key].items():

            if self._is_file_handler(handler_options):

                file_handler_path = handler_options[self._handler_filename_key]
                file_handler_absolute_path = self._get_absolute_path(file_handler_path)
                self._update_file_handler_path(handler_name, file_handler_absolute_path)
                self._create_file_handler_directory(file_handler_absolute_path)

    def _is_file_handler(self, handler_options: dict) -> bool:

        return self._handler_filename_key in handler_options

    def _get_absolute_path(self, path: str) -> str:

        if os.path.isabs(path):

            return os.path.normpath(path)

        else:

            return os.path.normpath(os.path.join(self._root_path, path))

    def _update_file_handler_path(self, handler_name: str, handler_path: str) -> None:

        self._config[self._config_handlers_key][handler_name][self._handler_filename_key] = handler_path

    @staticmethod
    def _create_file_handler_directory(file_handler_path: str) -> None:

        os.makedirs(os.path.dirname(file_handler_path), exist_ok=True)
