from .audio_controller import AudioController
from .search_controller import SearchController
from ..tools.typing import ControllerClassType


app_controllers: list[ControllerClassType] = [AudioController, SearchController]
