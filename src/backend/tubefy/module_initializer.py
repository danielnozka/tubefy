from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from .adapters import AudioRecordingAdapter, AudioSampleAdapter, TokenAdapter, UserAdapter, YoutubeVideosAdapter
from .app import APP_ROOT_PATH, APP_SETTINGS_FILE_PATH
from .communications import YoutubeAudioDownloader, YoutubeVideosGetter
from .configuration import AppSettings
from .persistence import AudioRecordingsPersistence, AudioSamplesPersistence, UsersPersistence
from .services import DirectoryHandler, JsonWebTokenHandler, LoggingHandler, PasswordHashHandler
from .use_cases import (
    AudioRecordingAdder,
    AudioRecordingDeleter,
    AudioRecordingGetter,
    AudioSampleGetter,
    UserGetter,
    UserLoginHandler,
    UserRegistrationHandler,
    VideoSearchHandler
)


class ModuleInitializer(DeclarativeContainer):

    audio_recording_adapter: Singleton[AudioRecordingAdapter] = Singleton(AudioRecordingAdapter)
    audio_sample_adapter: Singleton[AudioSampleAdapter] = Singleton(AudioSampleAdapter)
    token_adapter: Singleton[TokenAdapter] = Singleton(TokenAdapter)
    user_adapter: Singleton[UserAdapter] = Singleton(UserAdapter)
    youtube_videos_adapter: Singleton[YoutubeVideosAdapter] = Singleton(YoutubeVideosAdapter)
    youtube_audio_downloader: Singleton[YoutubeAudioDownloader] = Singleton(YoutubeAudioDownloader)
    youtube_videos_getter: Singleton[YoutubeVideosGetter] = Singleton(YoutubeVideosGetter)
    app_settings: Singleton[AppSettings] = Singleton(AppSettings, settings_file_path=APP_SETTINGS_FILE_PATH)
    audio_recordings_persistence: Singleton[AudioRecordingsPersistence] = Singleton(AudioRecordingsPersistence)
    audio_samples_persistence: Singleton[AudioSamplesPersistence] = Singleton(AudioSamplesPersistence)
    users_persistence: Singleton[UsersPersistence] = Singleton(UsersPersistence)
    directory_handler: Singleton[DirectoryHandler] = Singleton(DirectoryHandler, root_path=APP_ROOT_PATH)
    json_web_token_handler: Singleton[JsonWebTokenHandler] = Singleton(JsonWebTokenHandler)
    logging_handler: Singleton[LoggingHandler] = Singleton(LoggingHandler)
    password_hash_handler: Singleton[PasswordHashHandler] = Singleton(PasswordHashHandler)
    audio_recording_adder: Singleton[AudioRecordingAdder] = Singleton(AudioRecordingAdder)
    audio_recording_deleter: Singleton[AudioRecordingDeleter] = Singleton(AudioRecordingDeleter)
    audio_recording_getter: Singleton[AudioRecordingGetter] = Singleton(AudioRecordingGetter)
    audio_sample_getter: Singleton[AudioSampleGetter] = Singleton(AudioSampleGetter)
    user_getter: Singleton[UserGetter] = Singleton(UserGetter)
    user_login_handler: Singleton[UserLoginHandler] = Singleton(UserLoginHandler)
    user_registration_handler: Singleton[UserRegistrationHandler] = Singleton(UserRegistrationHandler)
    video_search_handler: Singleton[VideoSearchHandler] = Singleton(VideoSearchHandler)
