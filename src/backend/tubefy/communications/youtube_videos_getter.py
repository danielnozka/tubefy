import logging
from logging import Logger
from youtube_search import YoutubeSearch
from ..exceptions.youtube_video_search_exception import YoutubeVideoSearchException


logging.getLogger('urllib3').propagate = False


class YoutubeVideosGetter:

    _log: Logger = logging.getLogger(__name__)
    _max_results: int = 20

    def get(self, query: str) -> list[dict[str, str | list[str]]]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')

        try:

            result: list[dict[str, str | list[str]]] = YoutubeSearch(
                search_terms=query,
                max_results=self._max_results
            ).to_dict()
            self._log.debug(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            raise YoutubeVideoSearchException(exception)
