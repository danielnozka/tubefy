import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..dtos.output_search_result import OutputSearchResult
from ..tools.server import http_get
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.search_service import SearchService


@route('/search')
class SearchController:

    _log: Logger = logging.getLogger(__name__)
    _search_service: SearchService

    @inject
    def __init__(self, search_service: SearchService = Provide['search_service']):

        self._search_service = search_service

    @http_get('')
    @return_json
    def search_videos(self, query: str) -> list[OutputSearchResult]:

        self._log.info(f'Start [funcName](query=\'{query}\')')

        try:

            result = self._search_service.search(query)
            self._log.info(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](query=\'{query}\') with exceptions', extra={'exception': exception})

            return_exception(exception)
