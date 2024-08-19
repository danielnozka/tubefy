import logging
from logging import Logger
from ..domain.video import Video
from ..dtos.video_dto import VideoDto


class VideoAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_video_to_dto(self, video: Video) -> VideoDto:

        self._log.debug(f'Start [funcName](video={video})')
        result: VideoDto = VideoDto(id=video.id, title=video.title, thumbnail_url=video.thumbnail_url)
        self._log.debug(f'End [funcName](video={video})')

        return result
