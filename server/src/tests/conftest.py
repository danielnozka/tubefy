import os
import pkgutil
import pytest
import shutil

from dependency_injector.providers import Singleton
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from . import fixtures
from . import audio_service_test
from . import search_service_test
from youtube_audio_manager_server import main as app_module
from youtube_audio_manager_server.configuration.app_settings import AppSettings
from youtube_audio_manager_server.main import Main as App
from youtube_audio_manager_server.module_initializer import app_components
from youtube_audio_manager_server.module_initializer import ModuleInitializer
from youtube_audio_manager_server.module_initializer import root_path


test_settings_file: str = os.path.join(os.path.dirname(__file__), 'test_app_settings.json')
pytest_plugins: list[str] = [f'{fixtures.__name__}.{module}' for _, module, _ in pkgutil.iter_modules(['./fixtures'])]


@pytest.fixture(scope='session', autouse=True)
def setup_module_initializer() -> None:

    modules_to_wire = [__name__, app_module, audio_service_test, search_service_test]
    packages_to_wire = [fixtures, *app_components]
    module_initializer_ = ModuleInitializer()
    module_initializer_.wire(modules=modules_to_wire, packages=packages_to_wire)
    module_initializer_.app_settings.override(Singleton(AppSettings, root_path, test_settings_file))


@pytest.fixture(scope='session', autouse=True)
def setup(setup_module_initializer: None) -> None:

    app = App()
    app.start(testing=True)
    yield
    app.stop()
    teardown()


@inject
def teardown(app_settings: AppSettings = Provide['app_settings']) -> None:

    delete_directory(app_settings.persistence_settings.audio_database_directory)
    delete_directory(app_settings.persistence_settings.audio_files_directory)


def delete_directory(directory: str) -> None:

    if os.path.isdir(directory):

        shutil.rmtree(directory)
