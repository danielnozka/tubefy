from .app_base_controller import AppBaseController
from .user_audio_controller import UserAudioController
from .user_authentication_controller import UserAuthenticationController
from .video_handler_controller import VideoHandlerController


APP_CONTROLLERS: list[type[AppBaseController]] = [
    UserAudioController,
    UserAuthenticationController,
    VideoHandlerController
]
