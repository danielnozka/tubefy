import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import UUID

from ..dtos.output_audio_recording import OutputAudioRecording
from ..tools.server import expect_json
from ..tools.server import get_json_content
from ..tools.server import http_delete
from ..tools.server import http_get
from ..tools.server import http_put
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.audio_service import AudioService


@route('/users/{user_id}/audio')
class AudioController:

    _log: Logger = logging.getLogger(__name__)
    _audio_service: AudioService

    @inject
    def __init__(self, audio_service: AudioService = Provide['audio_service']):

        self._audio_service = audio_service

    @http_put('/{video_id}')
    @expect_json
    def download_audio_recording(self, user_id: UUID, video_id: str) -> None:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        try:

            self._audio_service.download_audio_recording(user_id, video_id, get_json_content())
            self._log.info(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)

    @http_get('/')
    @return_json
    def get_all_audio_recordings(self, user_id: UUID) -> list[OutputAudioRecording]:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\')')

        try:

            result = self._audio_service.get_all_audio_recordings(user_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\') with exceptions', extra={'exception': exception})

            return_exception(exception)

    @http_delete('/{video_id}')
    def delete_audio_recording(self, user_id: UUID, video_id: str) -> None:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        try:

            self._audio_service.delete_audio_recording(user_id, video_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)
