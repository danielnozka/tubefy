import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from logging import Logger

from .app_base_controller import AppBaseController
from ..dtos import AudioOutput, VideoOutput
from ..use_cases import AudioSampleGetter, AudioSamplesDeleter, VideoSearchHandler


class VideoHandlerController(AppBaseController):

    api_router: APIRouter = APIRouter(prefix='/api/videos', tags=['video_handler'])
    _log: Logger = logging.getLogger(__name__)
    _audio_sample_getter: AudioSampleGetter
    _video_search_handler: VideoSearchHandler

    @inject
    def __init__(
        self,
        audio_sample_getter: AudioSampleGetter = Provide['audio_sample_getter'],
        audio_samples_deleter: AudioSamplesDeleter = Provide['audio_samples_deleter'],
        video_search_handler: VideoSearchHandler = Provide['video_search_handler']
    ):

        self.api_router.add_api_route(
            path='/search',
            endpoint=self.search_videos,
            methods=['GET']
        )
        self.api_router.add_api_route(
            path='/{video_id}/audio/sample',
            endpoint=self.get_audio_sample_from_video,
            methods=['GET']
        )
        self._audio_sample_getter = audio_sample_getter
        self._video_search_handler = video_search_handler
        audio_samples_deleter.delete()

    async def search_videos(self, query: str) -> list[VideoOutput]:

        self._log.info(f'Start [funcName](query=\'{query}\')')

        try:

            result: list[VideoOutput] = self._video_search_handler.search(query)
            self._log.info(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](query=\'{query}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception

    async def get_audio_sample_from_video(self, video_id: str) -> AudioOutput:

        self._log.info(f'Start [funcName](video_id=\'{video_id}\')')

        try:

            result: AudioOutput = self._audio_sample_getter.get(video_id)
            self._log.info(f'End [funcName](video_id=\'{video_id}\')')

            return result

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](video_id=\'{video_id}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception
