import logging

from logging import Logger
from youtube_search import YoutubeSearch

from ..exceptions import YoutubeSearchException


logging.getLogger('urllib3').propagate = False


class YoutubeVideosGetter:

    _log: Logger = logging.getLogger(__name__)
    _max_results: int = 20

    def get(self, query: str) -> list[dict]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')

        try:

            result = YoutubeSearch(query, self._max_results).to_dict()
            self._log.debug(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            raise YoutubeSearchException(exception)
