import requests

from fastapi.testclient import TestClient
from httpx import Response
from unittest import mock
from youtube_search import YoutubeSearch


class VideoSearchHandlerTest:

    _search_query: str = 'rick astley never gonna give you up'
    _end_point: str = f'/api/videos/search?query={_search_query}'
    _result_video_id: str = 'dQw4w9WgXcQ'

    def test_youtube_video_search_exception_is_caught(self, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeSearch, attribute='__init__', side_effect=Exception('Test exception')):

            response = self._request_video_search(test_client)
            assert response.status_code == 500

    def test_search_results_are_returned(self, test_client: TestClient) -> None:

        response = self._request_video_search(test_client)
        assert response.status_code == 200
        json_response = response.json()
        assert type(json_response) == list
        assert len(json_response) > 0
        assert any([result.get('id') == self._result_video_id for result in json_response])
        assert all([requests.get(result.get('thumbnailUrl')).status_code == 200 for result in json_response])

    def _request_video_search(self, test_client: TestClient) -> Response:

        return test_client.get(self._end_point)
