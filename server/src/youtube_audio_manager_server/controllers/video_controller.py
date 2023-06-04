import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..dtos.output_video_search_result import OutputVideoSearchResult
from ..tools.server import http_get
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.video_service import VideoService


@route('/video')
class VideoController:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self, video_service: VideoService = Provide['video_service']):

        self._video_service = video_service

    @http_get('/')
    @return_json
    def search_videos(self, search_query: str) -> list[OutputVideoSearchResult]:

        self._log.debug(f'Start [funcName](search_query=\'{search_query}\')')

        try:

            result = self._video_service.search_videos(search_query)
            self._log.debug(f'End [funcName](search_query=\'{search_query}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](search_query=\'{search_query}\') with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)
