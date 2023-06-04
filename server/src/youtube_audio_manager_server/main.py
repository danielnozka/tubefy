import logging
import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from .configuration.app_settings import AppSettings
from .controllers import app_controllers
from .exceptions.server_stopped_exception import ServerStoppedException
from .module_initializer import app_components
from .module_initializer import ModuleInitializer
from .server import Server
from .tools.logging.logging_builder import LoggingBuilder


class Main:

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        LoggingBuilder(app_settings.root_path, os.path.join(app_settings.root_path, 'log_settings.json')).configure()
        self._log = logging.getLogger(__name__)
        self._server = Server(app_settings.root_path,
                              app_settings.server_settings.host,
                              app_settings.server_settings.port)

    def start(self, testing: bool = False) -> None:

        self._log.debug('Starting application...')

        try:

            self._register_controllers()
            self._server.start(testing)

        except ServerStoppedException:

            self._log.error('Stopped application because of server exception')

    def stop(self) -> None:

        self._log.debug('Stopping application...')
        self._server.stop()

    def _register_controllers(self) -> None:

        for ControllerClass in app_controllers:

            self._server.register_controller(ControllerClass())


if __name__ == '__main__':

    module_initializer = ModuleInitializer()
    module_initializer.wire(modules=[__name__], packages=app_components)
    main = Main()
    main.start()
