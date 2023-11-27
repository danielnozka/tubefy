import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..dtos import VideoAudioOutput, VideoOutput
from ..server import BaseController, http_get, route
from ..use_cases import VideoAudioSampleGetter, VideoSearchHandler


@route('/api/videos')
class VideoHandlerController(BaseController):

    _log: Logger = logging.getLogger(__name__)
    _video_audio_sample_getter: VideoAudioSampleGetter
    _video_search_handler: VideoSearchHandler

    @inject
    def __init__(
        self,
        video_audio_sample_getter: VideoAudioSampleGetter = Provide['video_audio_sample_getter'],
        video_search_handler: VideoSearchHandler = Provide['video_search_handler']
    ):

        self._video_audio_sample_getter = video_audio_sample_getter
        self._video_search_handler = video_search_handler

    @http_get('/search')
    def search_videos(self, query: str) -> list[VideoOutput]:

        self._log.info(f'Start [funcName](query=\'{query}\')')

        try:

            result = self._video_search_handler.search(query)
            self._log.info(f'End [funcName](query=\'{query}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](query=\'{query}\') with exceptions', extra={'exception': exception})

    @http_get('/{video_id}/audio')
    def get_video_audio_sample(self, video_id: str) -> VideoAudioOutput:

        self._log.info(f'Start [funcName](video_id=\'{video_id}\')')

        try:

            result = self._video_audio_sample_getter.get(video_id)
            self._log.info(f'End [funcName](video_id=\'{video_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](video_id=\'{video_id}\') with exceptions', extra={'exception': exception})
