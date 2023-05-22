import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from . import adapters
from . import controllers
from . import persistence
from . import use_cases

from .adapters.music_adapter import MusicAdapter
from .configuration.app_settings import AppSettings
from .persistence.music_persistence import MusicPersistence
from .use_cases.music_downloader import MusicDownloader
from .use_cases.music_service import MusicService


app_components = [adapters, controllers, persistence, use_cases]
root_path = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    app_settings = Singleton(AppSettings,
                             root_path=root_path,
                             settings_file=os.path.join(root_path, 'app_settings.json'))

    music_adapter = Singleton(MusicAdapter)
    music_persistence = Singleton(MusicPersistence)
    music_downloader = Singleton(MusicDownloader)
    music_service = Singleton(MusicService)
