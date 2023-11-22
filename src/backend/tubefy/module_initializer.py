import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from types import ModuleType

from . import adapters
from . import communications
from . import controllers
from . import use_cases
from .adapters import YoutubeVideosAdapter
from .communications import YoutubeVideosGetter
from .configuration import AppSettings
from .use_cases import VideoSearchHandler


app_components: list[ModuleType] = [adapters, communications, controllers, use_cases]
root_path: str = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    youtube_videos_adapter = Singleton(YoutubeVideosAdapter)
    youtube_videos_getter = Singleton(YoutubeVideosGetter)
    app_settings = Singleton(
        AppSettings,
        root_path=root_path,
        settings_file=os.path.join(root_path, 'app_settings.json')
    )
    video_search_handler = Singleton(VideoSearchHandler)
