import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..adapters.video_search_adapter import VideoSearchAdapter
from ..communications.youtube_videos_getter import YoutubeVideosGetter
from ..dtos.output_video_search_result import OutputVideoSearchResult


class VideoSearchService:

    _log: Logger = logging.getLogger(__name__)
    _video_search_adapter: VideoSearchAdapter
    _youtube_videos_getter: YoutubeVideosGetter

    @inject
    def __init__(self,
                 video_search_adapter: VideoSearchAdapter = Provide['video_search_adapter'],
                 youtube_videos_getter: YoutubeVideosGetter = Provide['youtube_videos_getter']):

        self._video_search_adapter = video_search_adapter
        self._youtube_videos_getter = youtube_videos_getter

    def search_videos(self, query: str) -> list[OutputVideoSearchResult]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')
        search_result_message = self._youtube_videos_getter.get(query)
        result = self._video_search_adapter.adapt_output(search_result_message)
        self._log.debug(f'End [funcName](query=\'{query}\')')

        return result
