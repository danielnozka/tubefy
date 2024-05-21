import asyncio
import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.youtube_videos_adapter import YoutubeVideosAdapter
from ..communications.youtube_videos_getter import YoutubeVideosGetter
from ..dtos.video_output import VideoOutput


class VideoSearchHandler:

    _log: Logger = logging.getLogger(__name__)
    _youtube_videos_adapter: YoutubeVideosAdapter
    _youtube_videos_getter: YoutubeVideosGetter

    @inject
    def __init__(
        self,
        youtube_videos_adapter: YoutubeVideosAdapter = Provide['youtube_videos_adapter'],
        youtube_videos_getter: YoutubeVideosGetter = Provide['youtube_videos_getter']
    ) -> None:

        self._youtube_videos_adapter = youtube_videos_adapter
        self._youtube_videos_getter = youtube_videos_getter

    async def search(self, query: str) -> list[VideoOutput]:

        self._log.debug(f'Start [funcName](query=\'{query}\')')
        videos_message: list[dict] = await asyncio.to_thread(self._youtube_videos_getter.get, query)
        result: list[VideoOutput] = self._youtube_videos_adapter.adapt(videos_message)
        self._log.debug(f'End [funcName](query=\'{query}\')')

        return result
