import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..dtos.output_video_search_result import OutputVideoSearchResult
from ..tools.server import http_get
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.video_search_service import VideoSearchService


@route('/search')
class VideoSearchController:

    _log: Logger = logging.getLogger(__name__)
    _video_search_service: VideoSearchService

    @inject
    def __init__(self, video_search_service: VideoSearchService = Provide['video_search_service']):

        self._video_search_service = video_search_service

    @http_get('')
    @return_json
    def search_videos(self, query: str) -> list[OutputVideoSearchResult]:

        self._log.info(f'Start [funcName](query=\'{query}\')')

        try:

            result = self._video_search_service.search_videos(query)
            self._log.info(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](query=\'{query}\') with exceptions', extra={'exception': exception})

            return_exception(exception)
