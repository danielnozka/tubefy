import logging
import pkgutil
import pytest

from dependency_injector.wiring import inject, Provide

from . import fixtures
from tubefy import APP_COMPONENTS, ModuleInitializer
from tubefy.configuration import AppSettings
from tubefy.persistence import AudioRecordingsPersistence, AudioSamplesPersistence, UsersPersistence
from tubefy.services import DirectoryHandler, LoggingHandler


logging.getLogger('httpx').propagate = False

pytest_plugins: list[str] = [f'{fixtures.__name__}.{module}' for _, module, _ in pkgutil.iter_modules(['./fixtures'])]


@pytest.fixture(scope='session', autouse=True)
def setup() -> None:

    module_initializer: ModuleInitializer = ModuleInitializer()
    module_initializer.wire(modules=[__name__], packages=[*APP_COMPONENTS, fixtures])
    setup_logging()
    yield
    delete_test_data()


@inject
def setup_logging(logging_handler: LoggingHandler = Provide['logging_handler']) -> None:

    logging_handler.build()


@inject
def delete_test_data(
    app_settings: AppSettings = Provide['app_settings'],
    audio_recordings_persistence: AudioRecordingsPersistence = Provide['audio_recordings_persistence'],
    audio_samples_persistence: AudioSamplesPersistence = Provide['audio_samples_persistence'],
    users_persistence: UsersPersistence = Provide['users_persistence'],
    directory_handler: DirectoryHandler = Provide['directory_handler'],
    logging_handler: LoggingHandler = Provide['logging_handler']
) -> None:

    audio_recordings_persistence.close()
    audio_samples_persistence.close()
    users_persistence.close()
    logging_handler.close()
    directory_handler.delete_directory(app_settings.persistence_settings.data_path)
