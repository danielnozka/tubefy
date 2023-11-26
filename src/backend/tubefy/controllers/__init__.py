from .video_handler_controller import VideoHandlerController
from ..server import BaseController


app_controllers: list[type[BaseController]] = [
    VideoHandlerController
]
