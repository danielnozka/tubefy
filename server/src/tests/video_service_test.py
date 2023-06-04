import logging
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response

from youtube_audio_manager_server.configuration.app_settings import AppSettings


logging.getLogger('urllib3').propagate = False
logging.getLogger('urllib3').disabled = True


class VideoServiceTest:

    _video_route = 'video'
    _search_query_parameter = 'search_query'

    @classmethod
    def test_video_results_are_returned(cls, test_video_search_query: str, test_video_search_result: str) -> None:

        response = cls._request_video_results_to_be_returned(test_video_search_query)

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) > 0
        assert any([video.get('id') == test_video_search_result for video in json_response])

    @classmethod
    @inject
    def _request_video_results_to_be_returned(cls, test_video_search_query: str,
                                              app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = (f'http://localhost:{app_settings.server_settings.port}/{cls._video_route}/?{cls._search_query_parameter}'
               f'={test_video_search_query}')

        response = requests.get(url)

        return response
