import logging

from logging import Logger

from ..dtos.output_video_search_result import OutputVideoSearchResult


class VideoSearchAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_output(self, search_result_message: list[dict]) -> list[OutputVideoSearchResult]:

        self._log.debug('Start [funcName]()')

        result: list[OutputVideoSearchResult] = []

        for search_result_record in search_result_message:

            output_video_search_result = OutputVideoSearchResult(
                video_id=search_result_record['id'],
                video_title=search_result_record['title'],
                video_thumbnail_url=search_result_record['thumbnails'][0]
            )

            result.append(output_video_search_result)

        self._log.debug('End [funcName]()')

        return result
