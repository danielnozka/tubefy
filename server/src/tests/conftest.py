import os
import pkgutil
import pytest
import shutil

from dependency_injector.providers import Singleton
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from . import integration as integration_tests
from . import unit as unit_tests
from .integration import fixtures as integration_tests_fixtures
from .unit import fixtures as unit_tests_fixtures
from youtube_music_manager_server import main
from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.module_initializer import app_components
from youtube_music_manager_server.module_initializer import ModuleInitializer
from youtube_music_manager_server.module_initializer import root_path


test_settings_file = os.path.join(os.path.dirname(__file__), 'test_app_settings.json')
integration_tests_plugins = [f'tests.integration.fixtures.{module}'
                             for _, module, _ in pkgutil.iter_modules(['./integration/fixtures'])]
unit_tests_plugins = [f'tests.unit.fixtures.{module}'
                      for _, module, _ in pkgutil.iter_modules(['./unit/fixtures'])]
pytest_plugins = integration_tests_plugins + unit_tests_plugins


@pytest.fixture(scope='session', autouse=True)
def module_initializer() -> None:

    modules_to_wire = [__name__, main]
    packages_to_wire = [integration_tests, integration_tests_fixtures, unit_tests, unit_tests_fixtures, *app_components]

    module_initializer = ModuleInitializer()
    module_initializer.wire(modules=modules_to_wire, packages=packages_to_wire)
    module_initializer.app_settings.override(Singleton(AppSettings, root_path, test_settings_file))

    yield
    teardown()


@inject
def teardown(app_settings: AppSettings = Provide['app_settings']) -> None:

    delete_directory(app_settings.persistence_settings.music_database_directory)
    delete_directory(app_settings.persistence_settings.music_files_directory)


def delete_directory(directory: str) -> None:

    if os.path.isdir(directory):

        shutil.rmtree(directory)
