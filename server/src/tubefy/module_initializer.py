import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from types import ModuleType

from . import adapters
from . import communications
from . import controllers
from . import persistence
from . import use_cases
from .adapters.user_audio_adapter import UserAudioAdapter
from .adapters.video_search_adapter import VideoSearchAdapter
from .communications.youtube_audio_downloader import YoutubeAudioDownloader
from .communications.youtube_videos_getter import YoutubeVideosGetter
from .configuration.app_settings import AppSettings
from .persistence.sample_audio_persistence import SampleAudioPersistence
from .persistence.user_audio_persistence import UserAudioPersistence
from .use_cases.audio_player_service import AudioPlayerService
from .use_cases.user_audio_service import UserAudioService
from .use_cases.video_search_service import VideoSearchService


app_components: list[ModuleType] = [adapters, communications, controllers, persistence, use_cases]
root_path: str = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    app_settings = Singleton(AppSettings,
                             root_path=root_path,
                             settings_file=os.path.join(root_path, 'app_settings.json'))

    user_audio_adapter = Singleton(UserAudioAdapter)
    video_search_adapter = Singleton(VideoSearchAdapter)
    youtube_audio_downloader = Singleton(YoutubeAudioDownloader)
    youtube_videos_getter = Singleton(YoutubeVideosGetter)
    sample_audio_persistence = Singleton(SampleAudioPersistence)
    user_audio_persistence = Singleton(UserAudioPersistence)
    audio_player_service = Singleton(AudioPlayerService)
    user_audio_service = Singleton(UserAudioService)
    video_search_service = Singleton(VideoSearchService)
