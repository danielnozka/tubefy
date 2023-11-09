import logging
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response
from string import Template

from tubefy.configuration.app_settings import AppSettings
from tubefy.domain.audio_recording import AudioRecording


logging.getLogger('urllib3').propagate = False


class VideoSearchServiceTest:

    _search_end_point: Template = Template('/search?query=${query}')
    _sample_player_end_point: Template = Template('/player/videos/${video_id}')

    @classmethod
    def test_search_results_are_returned(cls, test_video_search_query: str,
                                         test_audio_recording: AudioRecording) -> None:

        response = cls._request_search_results_to_be_returned(test_video_search_query)

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) > 0
        assert any([result.get('videoId') == test_audio_recording.video_id for result in json_response])
        assert all([requests.get(result.get('videoThumbnailUrl')).status_code == 200 for result in json_response])

    @classmethod
    def test_sample_audio_is_played(cls, test_audio_recording: AudioRecording) -> None:

        response = cls._request_sample_audio_to_be_played(test_audio_recording)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'audio/mpeg'

    @classmethod
    @inject
    def _request_search_results_to_be_returned(cls, test_video_search_query: str,
                                               app_settings: AppSettings = Provide['app_settings']) -> Response:

        search_end_point = cls._search_end_point.substitute(query=test_video_search_query)
        url = f'http://localhost:{app_settings.server_settings.port}' + search_end_point
        response = requests.get(url)

        return response

    @classmethod
    @inject
    def _request_sample_audio_to_be_played(cls, test_audio_recording: AudioRecording,
                                           app_settings: AppSettings = Provide['app_settings']) -> Response:

        sample_player_end_point = cls._sample_player_end_point.substitute(video_id=test_audio_recording.video_id)
        url = f'http://localhost:{app_settings.server_settings.port}' + sample_player_end_point
        response = requests.get(url)

        return response
