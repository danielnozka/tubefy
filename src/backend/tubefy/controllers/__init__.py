from .video_handler_controller import VideoHandlerController
from ..server import BaseController


APP_CONTROLLERS: list[type[BaseController]] = [
    VideoHandlerController
]
