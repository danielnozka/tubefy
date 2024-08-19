import logging
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from logging import Logger
from ..adapters.video_adapter import VideoAdapter
from .app_base_controller import AppBaseController
from ..domain.audio import Audio
from ..domain.video import Video
from ..dtos.video_dto import VideoDto
from ..use_cases.audio_sample_getter import AudioSampleGetter
from ..use_cases.videos_getter import VideosGetter


class VideoController(AppBaseController):

    _api_router: APIRouter = APIRouter(prefix='/api/videos', tags=['video'])
    _log: Logger = logging.getLogger(__name__)
    _video_adapter: VideoAdapter

    def __init__(self) -> None:

        self._api_router.add_api_route(path='/search', endpoint=self.get_videos, methods=['GET'])
        self._api_router.add_api_route(path='/{video_id}/audio/sample', endpoint=self.get_audio_sample, methods=['GET'])
        self._video_adapter = VideoAdapter()

    @property
    def api_router(self) -> APIRouter:

        return self._api_router

    @inject
    async def get_videos(
        self,
        search_query: str,
        videos_getter: VideosGetter = Depends(Provide['videos_getter'])
    ) -> list[VideoDto]:

        self._log.info(f'Start [funcName](search_query=\'{search_query}\')')

        try:

            videos: list[Video] = await videos_getter.get_videos(search_query)
            result: list[VideoDto] = list(map(self._video_adapter.adapt_video_to_dto, videos))
            self._log.info(f'End [funcName](search_query=\'{search_query}\')')

            return result

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](search_query=\'{search_query}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception

    @inject
    async def get_audio_sample(
        self,
        video_id: str,
        audio_sample_getter: AudioSampleGetter = Provide['audio_sample_getter']
    ) -> FileResponse:

        self._log.info(f'Start [funcName](video_id=\'{video_id}\')')

        try:

            audio_sample: Audio = await audio_sample_getter.get_audio_sample(video_id)
            self._log.info(f'End [funcName](video_id=\'{video_id}\')')

            return FileResponse(audio_sample.file_path)

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](video_id=\'{video_id}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception
