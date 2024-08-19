import logging
from logging import Logger
from ..domain.video import Video
from ..services.i_videos_repository import IVideosRepository


class VideosGetter:

    _log: Logger = logging.getLogger(__name__)
    _videos_repository: IVideosRepository

    def __init__(self, videos_repository: IVideosRepository) -> None:

        self._videos_repository = videos_repository

    async def get_videos(self, search_query: str) -> list[Video]:

        self._log.debug(f'Start [funcName](search_query=\'{search_query}\')')
        result: list[Video] = await self._videos_repository.search_videos(search_query)
        self._log.debug(f'End [funcName](search_query=\'{search_query}\')')

        return result
