import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import UUID

from ..tools.server import http_get
from ..tools.server import return_audio
from ..tools.server import return_exception
from ..tools.server import route
from ..use_cases.audio_player_service import AudioPlayerService


@route('/player')
class AudioPlayerController:

    _log: Logger = logging.getLogger(__name__)
    _audio_player_service: AudioPlayerService

    @inject
    def __init__(self, audio_player_service: AudioPlayerService = Provide['audio_player_service']):

        self._audio_player_service = audio_player_service

    @http_get('/videos/{video_id}')
    @return_audio
    def play_audio_sample(self, video_id: str) -> bytes:

        self._log.info(f'Start [funcName](video_id=\'{video_id}\')')

        try:

            result = self._audio_player_service.play_audio_sample(video_id)
            self._log.info(f'End [funcName](video_id=\'{video_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](video_id=\'{video_id}\') with exceptions', extra={'exception': exception})

            return_exception(exception)

    @http_get('/users/{user_id}/recordings/{recording_id}')
    @return_audio
    def play_user_saved_audio(self, user_id: UUID, recording_id: UUID) -> bytes:

        self._log.info(f'Start [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

        try:

            result = self._audio_player_service.play_user_saved_audio(user_id, recording_id)
            self._log.info(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\') with exceptions',
                            extra={'exception': exception})

            return_exception(exception)
