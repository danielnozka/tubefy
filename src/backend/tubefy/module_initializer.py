from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from pathlib import Path
from types import ModuleType

from . import adapters
from . import communications
from . import configuration
from . import controllers
from . import services
from . import use_cases
from .adapters import YoutubeVideosAdapter
from .communications import YoutubeVideosGetter
from .configuration import AppSettings
from .services import DirectoryBuilder, LoggingBuilder
from .use_cases import VideoSearchHandler


APP_COMPONENTS: list[ModuleType] = [adapters, communications, configuration, controllers, services, use_cases]
ROOT_PATH: Path = Path(__file__).parent


class ModuleInitializer(DeclarativeContainer):

    youtube_videos_adapter = Singleton(YoutubeVideosAdapter)
    youtube_videos_getter = Singleton(YoutubeVideosGetter)
    app_settings = Singleton(AppSettings, root_path=ROOT_PATH)
    directory_builder = Singleton(DirectoryBuilder, root_path=ROOT_PATH)
    logging_builder = Singleton(LoggingBuilder, root_path=ROOT_PATH)
    video_search_handler = Singleton(VideoSearchHandler)
