import logging
import os

from dependency_injector.wiring import inject, Provide
from logging import Logger

from .configuration import AppSettings
from .controllers import app_controllers
from .module_initializer import app_components, ModuleInitializer
from .server import Server
from .tools.logging import LoggingBuilder


class Main:

    _log: Logger
    _server: Server

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        LoggingBuilder(app_settings.root_path, os.path.join(app_settings.root_path, 'log_settings.json')).configure()
        self._log = logging.getLogger(__name__)
        self._server = Server(app_settings.server_settings.host, app_settings.server_settings.port)

    def start(self) -> None:

        self._log.info('Starting application...')

        try:

            self._server.register_controllers(app_controllers)
            self._server.start()

        except Exception as exception:

            self._log.error('Stopped application because of exception', extra={'exception': exception})


if __name__ == '__main__':

    module_initializer = ModuleInitializer()
    module_initializer.wire(modules=[__name__], packages=app_components)
    main = Main()
    main.start()
