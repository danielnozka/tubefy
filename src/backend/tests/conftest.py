import logging
import pkgutil
import pytest
from dependency_injector.wiring import inject, Provide
from . import fixtures
from tubefy import app, APP_COMPONENTS, APP_ROOT_PATH
from tubefy.logging.logging_builder import LoggingBuilder
from tubefy.module_initializer import ModuleInitializer
from tubefy.services.directory_handler import DirectoryHandler
from tubefy.settings.app_settings import AppSettings


logging.getLogger('pytest_dependency').propagate = False

pytest_plugins: list[str] = [
    f'{fixtures.__name__}.{module}' for _, module, _ in pkgutil.iter_modules([fixtures.__path__[0]])
]


@pytest.fixture(scope='session')
def module_initializer() -> ModuleInitializer:

    module_initializer: ModuleInitializer = ModuleInitializer()
    module_initializer.configuration.app_root_path.from_value(APP_ROOT_PATH)
    module_initializer.wire(modules=[__name__, app], packages=[*APP_COMPONENTS, fixtures])

    return module_initializer


@pytest.fixture(scope='session', autouse=True)
def setup(module_initializer: ModuleInitializer) -> None:

    LoggingBuilder.build()
    yield
    teardown()


@inject
def teardown(
    directory_handler: DirectoryHandler = Provide['directory_handler'],
    app_settings: AppSettings = Provide['app_settings']
) -> None:

    directory_handler.delete_directory(app_settings.persistence_settings.data_path)
