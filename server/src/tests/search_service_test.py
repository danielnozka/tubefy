import logging
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response
from string import Template

from youtube_audio_manager_server.configuration.app_settings import AppSettings
from youtube_audio_manager_server.domain.audio_recording import AudioRecording


logging.getLogger('urllib3').propagate = False


class SearchServiceTest:

    _end_point: Template = Template('/search?query=${query}')

    @classmethod
    def test_search_results_are_returned(cls, test_search_query: str, test_audio_recording: AudioRecording) -> None:

        response = cls._request_search_results_to_be_returned(test_search_query)

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) > 0
        assert any([result.get('videoId') == test_audio_recording.video_id for result in json_response])
        assert all([requests.get(result.get('videoThumbnailUrl')).status_code == 200 for result in json_response])

    @classmethod
    @inject
    def _request_search_results_to_be_returned(cls, test_search_query: str,
                                               app_settings: AppSettings = Provide['app_settings']) -> Response:

        end_point = cls._end_point.substitute(query=test_search_query)
        url = f'http://localhost:{app_settings.server_settings.port}' + end_point
        response = requests.get(url)

        return response