from .videos_search_controller import VideoSearchController
from ..server import BaseController


app_controllers: list[type[BaseController]] = [
    VideoSearchController
]
