import json
import os
import pkgutil
import pytest
import shutil

from dependency_injector.providers import Singleton

from .unit import fixtures
from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.module_initializer import ModuleInitializer
from youtube_music_manager_server.module_initializer import root_path
from youtube_music_manager_server import persistence


test_settings_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'app_settings.json')
unit_tests_fixtures = [f'tests.unit.fixtures.{module}' for _, module, _ in pkgutil.iter_modules(['./unit/fixtures'])]
pytest_plugins = unit_tests_fixtures


def _open_settings_file(file: str) -> dict:

    with open(file, 'r') as open_file:

        settings = json.load(open_file)

    return settings


def _delete_directory(directory: str) -> None:

    if os.path.isdir(directory):

        shutil.rmtree(directory)


@pytest.fixture(scope='session', autouse=True)
def module_initializer() -> ModuleInitializer:

    module_initializer = ModuleInitializer()
    module_initializer.wire(packages=[fixtures, persistence])
    module_initializer.app_settings.override(Singleton(AppSettings, root_path, test_settings_file))

    yield module_initializer

    test_settings = _open_settings_file(test_settings_file)
    _delete_directory(test_settings['persistenceSettings']['musicDatabaseDirectory'])
    _delete_directory(test_settings['persistenceSettings']['musicFilesDirectory'])
