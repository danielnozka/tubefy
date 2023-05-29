import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

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


@route('/audio')
class AudioController:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self, audio_service: AudioService = Provide['audio_service']):

        self._audio_service = audio_service

    @http_put('/{audio_recording_id}')
    @expect_json
    def download_audio_recording(self, audio_recording_id: str) -> None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')

        try:

            self._audio_service.download_audio_recording(audio_recording_id, get_json_content())
            self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](audio_recording_id=\'{audio_recording_id}\') with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)

    @http_get('/')
    @return_json
    def get_all_audio_recordings(self) -> list[OutputAudioRecording]:

        self._log.debug('Start [funcName]()')

        try:

            result = self._audio_service.get_all_audio_recordings()
            self._log.debug('End [funcName]()')

            return result

        except Exception as exception:

            self._log.error('End [funcName]() with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)

    @http_delete('/{audio_recording_id}')
    def delete_audio_recording(self, audio_recording_id: str) -> None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')

        try:

            self._audio_service.delete_audio_recording(audio_recording_id)
            self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](audio_recording_id=\'{audio_recording_id}\') with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)
