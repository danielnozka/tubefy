import os
import pkgutil
import pytest
import shutil

from dependency_injector.providers import Singleton
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from . import unit as unit_tests_package
from .unit import fixtures as unit_tests_fixtures_package
from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.module_initializer import app_components
from youtube_music_manager_server.module_initializer import ModuleInitializer
from youtube_music_manager_server.module_initializer import root_path


test_settings_file = os.path.join(os.path.dirname(__file__), 'test_app_settings.json')
unit_tests_fixtures = [f'tests.unit.fixtures.{module}' for _, module, _ in pkgutil.iter_modules(['./unit/fixtures'])]
pytest_plugins = unit_tests_fixtures


@pytest.fixture(scope='session', autouse=True)
def module_initializer() -> ModuleInitializer:

    module_initializer = ModuleInitializer()
    modules_to_wire = [__name__]
    packages_to_wire = [unit_tests_package, unit_tests_fixtures_package] + app_components
    module_initializer.wire(modules=modules_to_wire, packages=packages_to_wire)
    module_initializer.app_settings.override(Singleton(AppSettings, root_path, test_settings_file))

    yield module_initializer
    teardown()


@inject
def teardown(app_settings: AppSettings = Provide['app_settings']) -> None:

    delete_directory(app_settings.persistence_settings.music_database_directory)
    delete_directory(app_settings.persistence_settings.music_files_directory)


def delete_directory(directory: str) -> None:

    if os.path.isdir(directory):

        shutil.rmtree(directory)
