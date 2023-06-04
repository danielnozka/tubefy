import logging

from youtube_search import YoutubeSearch

from ..exceptions.video_search_exception import VideoSearchException


class VideoGetter:

    _log = logging.getLogger(__name__)
    _max_results = 20

    def get(self, search_query: str) -> list[dict]:

        self._log.debug(f'Start [funcName](search_query=\'{search_query}\')')

        try:

            result = YoutubeSearch(search_query, self._max_results).to_dict()
            self._log.debug(f'End [funcName](search_query=\'{search_query}\')')

            return result

        except Exception as exception:

            raise VideoSearchException(exception)
