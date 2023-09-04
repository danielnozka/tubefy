from .audio_player_controller import AudioPlayerController
from .authentication_controller import AuthenticationController
from .user_audio_controller import UserAudioController
from .video_search_controller import VideoSearchController
from ..tools.typing import ControllerClassType


app_controllers: list[ControllerClassType] = [
    AudioPlayerController,
    AuthenticationController,
    UserAudioController,
    VideoSearchController
]
