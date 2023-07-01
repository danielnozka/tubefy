import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..adapters.search_adapter import SearchAdapter
from ..communications.youtube_videos_getter import YoutubeVideosGetter
from ..dtos.output_search_result import OutputSearchResult


class SearchService:

    _log: Logger = logging.getLogger(__name__)
    _search_adapter: SearchAdapter
    _youtube_videos_getter: YoutubeVideosGetter

    @inject
    def __init__(self,
                 search_adapter: SearchAdapter = Provide['search_adapter'],
                 youtube_videos_getter: YoutubeVideosGetter = Provide['youtube_videos_getter']):

        self._search_adapter = search_adapter
        self._youtube_videos_getter = youtube_videos_getter

    def search(self, query: str) -> list[OutputSearchResult]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')
        search_result_message = self._youtube_videos_getter.get(query)
        result = self._search_adapter.adapt_output(search_result_message)
        self._log.debug(f'End [funcName](query=\'{query}\')')

        return result
