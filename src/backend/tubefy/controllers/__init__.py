from .app_base_controller import AppBaseController
from .user_audio_controller import UserAudioController
from .authentication_controller import UserAuthenticationController
from .video_controller import VideoHandlerController


APP_CONTROLLERS: list[type[AppBaseController]] = [
    UserAudioController,
    UserAuthenticationController,
    VideoHandlerController
]
