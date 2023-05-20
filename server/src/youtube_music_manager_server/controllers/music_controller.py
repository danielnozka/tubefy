import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..tools.server import expect_json
from ..tools.server import get_json_content
from ..tools.server import http_delete
from ..tools.server import http_get
from ..tools.server import http_put
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..tools.typing import JsonType
from ..use_cases.music_service import MusicService


@route('/music')
class MusicController:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self, music_service: MusicService = Provide['music_service']):

        self._music_service = music_service

    @http_put('/{song_id}')
    @expect_json
    def download_song(self, song_id: str) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')

        try:

            self._music_service.download_song(song_id, get_json_content())
            self._log.debug(f'End [funcName](song_id=\'{song_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](song_id=\'{song_id}\') with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)

    @http_get('/')
    @return_json
    def get_all_songs(self) -> JsonType:

        self._log.debug('Start [funcName]()')

        try:

            result = self._music_service.get_all_songs()
            self._log.debug('End [funcName]()')

            return result

        except Exception as exception:

            self._log.error('End [funcName]() with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)

    @http_delete('/{song_id}')
    def delete_song(self, song_id: str) -> None:

        self._log.debug(f'Start [funcName](song_id=\'{song_id}\')')

        try:

            self._music_service.delete_song(song_id)
            self._log.debug(f'End [funcName](song_id=\'{song_id}\')')

        except Exception as exception:

            self._log.error(f'End [funcName](song_id=\'{song_id}\') with exceptions',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            return_exception(exception)
