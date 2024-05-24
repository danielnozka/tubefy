from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
from .adapters.audio_recording_adapter import AudioRecordingAdapter
from .adapters.audio_sample_adapter import AudioSampleAdapter
from .adapters.token_adapter import TokenAdapter
from .adapters.user_adapter import UserAdapter
from .adapters.youtube_videos_adapter import YoutubeVideosAdapter
from .communications.youtube_audio_recording_getter import YoutubeAudioRecordingGetter
from .communications.youtube_audio_sample_getter import YoutubeAudioSampleGetter
from .communications.youtube_videos_getter import YoutubeVideosGetter
from .persistence.app_persistence_context import AppPersistenceContext
from .persistence.audio_recordings_persistence import AudioRecordingsPersistence
from .persistence.audio_samples_persistence import AudioSamplesPersistence
from .persistence.users_persistence import UsersPersistence
from .services.directory_handler import DirectoryHandler
from .services.json_web_token_handler import JsonWebTokenHandler
from .services.password_hash_handler import PasswordHashHandler
from .settings.app_settings import AppSettings
from .use_cases.audio_recording_adder import AudioRecordingAdder
from .use_cases.audio_recording_deleter import AudioRecordingDeleter
from .use_cases.audio_recording_getter import AudioRecordingGetter
from .use_cases.audio_sample_getter import AudioSampleGetter
from .use_cases.audio_samples_deleter import AudioSamplesDeleter
from .use_cases.user_getter import UserGetter
from .use_cases.user_login_handler import UserLoginHandler
from .use_cases.user_registration_handler import UserRegistrationHandler
from .use_cases.video_search_handler import VideoSearchHandler


class ModuleInitializer(DeclarativeContainer):

    # Configuration
    configuration: Configuration = Configuration()

    # Adapters
    audio_recording_adapter: Singleton[AudioRecordingAdapter] = Singleton(AudioRecordingAdapter)
    audio_sample_adapter: Singleton[AudioSampleAdapter] = Singleton(AudioSampleAdapter)
    token_adapter: Singleton[TokenAdapter] = Singleton(TokenAdapter)
    user_adapter: Singleton[UserAdapter] = Singleton(UserAdapter)
    youtube_videos_adapter: Singleton[YoutubeVideosAdapter] = Singleton(YoutubeVideosAdapter)

    # Communications
    youtube_audio_recording_getter: Singleton[YoutubeAudioRecordingGetter] = Singleton(YoutubeAudioRecordingGetter)
    youtube_audio_sample_getter: Singleton[YoutubeAudioSampleGetter] = Singleton(YoutubeAudioSampleGetter)
    youtube_videos_getter: Singleton[YoutubeVideosGetter] = Singleton(YoutubeVideosGetter)

    # Persistence
    app_persistence_context: Singleton[AppPersistenceContext] = Singleton(AppPersistenceContext)
    audio_recordings_persistence: Singleton[AudioRecordingsPersistence] = Singleton(AudioRecordingsPersistence)
    audio_samples_persistence: Singleton[AudioSamplesPersistence] = Singleton(AudioSamplesPersistence)
    users_persistence: Singleton[UsersPersistence] = Singleton(UsersPersistence)

    # Services
    directory_handler: Singleton[DirectoryHandler] = Singleton(DirectoryHandler, root_path=configuration.app_root_path)
    json_web_token_handler: Singleton[JsonWebTokenHandler] = Singleton(JsonWebTokenHandler)
    password_hash_handler: Singleton[PasswordHashHandler] = Singleton(PasswordHashHandler)

    # Settings
    app_settings: Singleton[AppSettings] = Singleton(AppSettings)

    # Use cases
    audio_recording_adder: Singleton[AudioRecordingAdder] = Singleton(AudioRecordingAdder)
    audio_recording_deleter: Singleton[AudioRecordingDeleter] = Singleton(AudioRecordingDeleter)
    audio_recording_getter: Singleton[AudioRecordingGetter] = Singleton(AudioRecordingGetter)
    audio_sample_getter: Singleton[AudioSampleGetter] = Singleton(AudioSampleGetter)
    audio_samples_deleter: Singleton[AudioSamplesDeleter] = Singleton(AudioSamplesDeleter)
    user_getter: Singleton[UserGetter] = Singleton(UserGetter)
    user_login_handler: Singleton[UserLoginHandler] = Singleton(UserLoginHandler)
    user_registration_handler: Singleton[UserRegistrationHandler] = Singleton(UserRegistrationHandler)
    video_search_handler: Singleton[VideoSearchHandler] = Singleton(VideoSearchHandler)
