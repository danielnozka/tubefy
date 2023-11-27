import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from .configuration import AppSettings
from .controllers import APP_CONTROLLERS
from .module_initializer import APP_COMPONENTS, ModuleInitializer
from .server import Server
from .services import LoggingBuilder


class Main:

    _log: Logger
    _server: Server

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        logging_builder: LoggingBuilder = Provide['logging_builder']
    ):

        logging_builder.build()
        self._log = logging.getLogger(__name__)
        self._server = Server(app_settings.server_settings.host, app_settings.server_settings.port)

    def start(self) -> None:

        self._log.info('Starting application...')

        try:

            self._server.register_controllers(APP_CONTROLLERS)
            self._server.start()

        except Exception as exception:

            self._log.error('Stopped application because of exception', extra={'exception': exception})


if __name__ == '__main__':

    module_initializer = ModuleInitializer()
    module_initializer.wire(modules=[__name__], packages=APP_COMPONENTS)
    main = Main()
    main.start()
