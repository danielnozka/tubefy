import logging


from ..dtos.output_video_search_result import OutputVideoSearchResult


class VideoAdapter:

    _log = logging.getLogger(__name__)

    def adapt_output(self, search_result: list[dict]) -> list[OutputVideoSearchResult]:

        self._log.debug('Start [funcName]()')

        result = []

        for video_search_result in search_result:

            output_video_search_result = OutputVideoSearchResult(video_search_result['id'])
            result.append(output_video_search_result)

        self._log.debug('End [funcName]()')

        return result
