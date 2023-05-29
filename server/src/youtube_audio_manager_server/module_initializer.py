import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from . import adapters
from . import controllers
from . import persistence
from . import use_cases

from .adapters.audio_adapter import AudioAdapter
from .configuration.app_settings import AppSettings
from .persistence.audio_persistence import AudioPersistence
from .use_cases.audio_downloader import AudioDownloader
from .use_cases.audio_service import AudioService


app_components = [adapters, controllers, persistence, use_cases]
root_path = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    app_settings = Singleton(AppSettings,
                             root_path=root_path,
                             settings_file=os.path.join(root_path, 'app_settings.json'))

    audio_adapter = Singleton(AudioAdapter)
    audio_persistence = Singleton(AudioPersistence)
    audio_downloader = Singleton(AudioDownloader)
    audio_service = Singleton(AudioService)
