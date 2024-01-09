from dependency_injector.wiring import inject, Provide

from .app import App, APP_COMPONENTS
from .configuration.app_settings import AppSettings
from .module_initializer import ModuleInitializer
from .services.logging_handler import LoggingHandler


@inject
def main(
    app_settings: AppSettings = Provide['app_settings'],
    logging_handler: LoggingHandler = Provide['logging_handler']
) -> None:

    logging_handler.build()
    app: App = App(host=app_settings.server_settings.host, port=app_settings.server_settings.port)
    app.start()


module_initializer: ModuleInitializer = ModuleInitializer()
module_initializer.wire(modules=[__name__], packages=APP_COMPONENTS)
main()
