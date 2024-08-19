from . import app, APP_COMPONENTS, APP_ROOT_PATH
from .app import App
from .logging.logging_builder import LoggingBuilder
from .container import ModuleInitializer


LoggingBuilder.build()
module_initializer: ModuleInitializer = ModuleInitializer()
module_initializer.configuration.app_root_path.from_value(APP_ROOT_PATH)
module_initializer.wire(modules=[app], packages=APP_COMPONENTS)
App().start()
