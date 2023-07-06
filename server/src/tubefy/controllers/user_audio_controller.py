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
from ..tools.server import return_audio
from ..tools.server import return_downloadable_file
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.user_audio_service import UserAudioService


@route('/audio/users/{user_id}')
class UserAudioController:

    _log: Logger = logging.getLogger(__name__)
    _user_audio_service: UserAudioService

    @inject
    def __init__(self, user_audio_service: UserAudioService = Provide['user_audio_service']):

        self._user_audio_service = user_audio_service

    @http_put('/videos/{video_id}')
    @expect_json
    def save_user_audio_recording(self, user_id: UUID, video_id: str) -> None:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        try:

            self._user_audio_service.save_user_audio_recording(user_id, video_id, get_json_content())
            self._log.info(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)

    @http_get('/recordings')
    @return_json
    def get_all_user_audio_recordings(self, user_id: UUID) -> list[OutputAudioRecording]:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\')')

        try:

            result = self._user_audio_service.get_all_user_audio_recordings(user_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\') with exceptions', extra={'exception': exception})

            return_exception(exception)

    @http_delete('/recordings/{recording_id}')
    def delete_user_audio_recording(self, user_id: UUID, recording_id: UUID) -> None:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

        try:

            self._user_audio_service.delete_user_audio_recording(user_id, recording_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)

    @http_get('/recordings/{recording_id}')
    @return_audio
    @return_downloadable_file
    def download_user_audio_recording(self, user_id: UUID, recording_id: UUID) -> bytes:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

        try:

            result = self._user_audio_service.download_user_audio_recording(user_id, recording_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)
