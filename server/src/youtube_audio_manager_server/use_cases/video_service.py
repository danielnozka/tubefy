import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..adapters.video_adapter import VideoAdapter
from ..dtos.output_video_search_result import OutputVideoSearchResult
from .video_getter import VideoGetter


class VideoService:

    _log: Logger = logging.getLogger(__name__)
    _video_adapter: VideoAdapter
    _video_getter: VideoGetter

    @inject
    def __init__(self,
                 video_adapter: VideoAdapter = Provide['video_adapter'],
                 video_getter: VideoGetter = Provide['video_getter']):

        self._video_adapter = video_adapter
        self._video_getter = video_getter

    def search_videos(self, search_query: str) -> list[OutputVideoSearchResult]:

        self._log.info(f'Start [funcName](search_query=\'{search_query}\')')
        search_result = self._video_getter.get(search_query)
        result = self._video_adapter.adapt_output(search_result)
        self._log.info(f'End [funcName](search_query=\'{search_query}\')')

        return result
