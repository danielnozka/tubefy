import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..dtos import VideoOutput
from ..server import BaseController, http_get, route
from ..use_cases import VideoSearchHandler


@route('/api/search')
class VideoSearchController(BaseController):

    _log: Logger = logging.getLogger(__name__)
    _video_searcher_handler: VideoSearchHandler

    @inject
    def __init__(self, video_searcher_handler: VideoSearchHandler = Provide['video_search_handler']):

        self._video_searcher_handler = video_searcher_handler

    @http_get('')
    def search_videos(self, query: str) -> list[VideoOutput]:

        self._log.info(f'Start [funcName](query=\'{query}\')')

        try:

            result = self._video_searcher_handler.search(query)
            self._log.info(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](query=\'{query}\') with exceptions', extra={'exception': exception})
