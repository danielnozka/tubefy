import logging

from logging import Logger

from ..dtos import VideoOutput


class YoutubeVideosAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt(self, videos_message: list[dict]) -> list[VideoOutput]:

        self._log.debug('Start [funcName]()')

        result: list[VideoOutput] = []

        for video in videos_message:

            video_output: VideoOutput = VideoOutput(
                id=video['id'],
                title=video['title'],
                thumbnail_url=video['thumbnails'][0]
            )
            result.append(video_output)

        self._log.debug('End [funcName]()')

        return result
