import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters import YoutubeVideosAdapter
from ..communications import YoutubeVideosGetter
from ..dtos import VideoOutput


class VideoSearchHandler:

    _log: Logger = logging.getLogger(__name__)
    _youtube_videos_adapter: YoutubeVideosAdapter
    _youtube_videos_getter: YoutubeVideosGetter

    @inject
    def __init__(
        self,
        youtube_videos_adapter: YoutubeVideosAdapter = Provide['youtube_videos_adapter'],
        youtube_videos_getter: YoutubeVideosGetter = Provide['youtube_videos_getter']
    ):

        self._youtube_videos_adapter = youtube_videos_adapter
        self._youtube_videos_getter = youtube_videos_getter

    def search(self, query: str) -> list[VideoOutput]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')
        videos_message = self._youtube_videos_getter.get(query)
        result = self._youtube_videos_adapter.adapt(videos_message)
        self._log.debug(f'End [funcName](query=\'{query}\')')

        return result
