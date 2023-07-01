import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from types import ModuleType

from . import adapters
from . import communications
from . import controllers
from . import persistence
from . import use_cases
from .adapters.audio_adapter import AudioAdapter
from .adapters.search_adapter import SearchAdapter
from .communications.youtube_videos_getter import YoutubeVideosGetter
from .configuration.app_settings import AppSettings
from .persistence.audio_persistence import AudioPersistence
from .use_cases.audio_downloader import AudioDownloader
from .use_cases.audio_service import AudioService
from .use_cases.search_service import SearchService


app_components: list[ModuleType] = [adapters, communications, controllers, persistence, use_cases]
root_path: str = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    app_settings = Singleton(AppSettings,
                             root_path=root_path,
                             settings_file=os.path.join(root_path, 'app_settings.json'))

    audio_adapter = Singleton(AudioAdapter)
    search_adapter = Singleton(SearchAdapter)
    youtube_videos_getter = Singleton(YoutubeVideosGetter)
    audio_persistence = Singleton(AudioPersistence)
    audio_downloader = Singleton(AudioDownloader)
    audio_service = Singleton(AudioService)
    search_service = Singleton(SearchService)
