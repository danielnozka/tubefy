import asyncio
import logging
from logging import Logger
from typing import TypeAlias
from youtube_search import YoutubeSearch
from ..domain.video import Video
from ..exceptions.youtube_videos_repository_exception import YoutubeVideosRepositoryException
from .i_videos_repository import IVideosRepository


YoutubeVideo: TypeAlias = dict[str, str | list[str]]


class YoutubeVideosRepository(IVideosRepository):

    _log: Logger = logging.getLogger(__name__)
    _max_results: int = 20

    async def search_videos(self, search_query: str) -> list[Video]:

        self._log.debug(f'Start [funcName](search_query=\'{search_query}\')')

        try:

            result: list[Video] = []
            youtube_videos: list[YoutubeVideo] = (
                await asyncio.to_thread(YoutubeSearch, search_terms=search_query, max_results=self._max_results)
            ).to_dict()

            youtube_video: YoutubeVideo
            for video in youtube_videos:

                result.append(Video(id=video['id'], title=video['title'], thumbnail_url=video['thumbnails'][0]))

            self._log.debug(f'End [funcName](search_query=\'{search_query}\')')

            return result

        except Exception as exception:

            raise YoutubeVideosRepositoryException(exception)
