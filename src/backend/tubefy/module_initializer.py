from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from pathlib import Path
from types import ModuleType

from . import adapters
from . import communications
from . import configuration
from . import controllers
from . import persistence
from . import services
from . import use_cases
from .adapters import VideoAudioAdapter, YoutubeVideosAdapter
from .communications import YoutubeAudioDownloader, YoutubeVideosGetter
from .configuration import AppSettings
from .persistence import VideoAudioSamplePersistence
from .services import DirectoryBuilder, LoggingBuilder
from .use_cases import VideoAudioSampleGetter, VideoSearchHandler


APP_COMPONENTS: list[ModuleType] = [
    adapters,
    communications,
    configuration,
    controllers,
    persistence,
    services,
    use_cases
]
ROOT_PATH: Path = Path(__file__).parent


class ModuleInitializer(DeclarativeContainer):

    video_audio_adapter = Singleton(VideoAudioAdapter)
    youtube_videos_adapter = Singleton(YoutubeVideosAdapter)
    youtube_audio_downloader = Singleton(YoutubeAudioDownloader)
    youtube_videos_getter = Singleton(YoutubeVideosGetter)
    app_settings = Singleton(AppSettings, root_path=ROOT_PATH)
    video_audio_sample_persistence = Singleton(VideoAudioSamplePersistence)
    directory_builder = Singleton(DirectoryBuilder, root_path=ROOT_PATH)
    logging_builder = Singleton(LoggingBuilder, root_path=ROOT_PATH)
    video_audio_sample_getter = Singleton(VideoAudioSampleGetter)
    video_search_handler = Singleton(VideoSearchHandler)
