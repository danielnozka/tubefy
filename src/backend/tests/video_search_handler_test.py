import requests

from fastapi.testclient import TestClient
from httpx import Response
from unittest import mock
from youtube_search import YoutubeSearch


class VideoSearchHandlerTest:

    _search_query: str = 'rick astley never gonna give you up'
    _end_point: str = f'/api/videos/search?query={_search_query}'
    _result_video_id: str = 'dQw4w9WgXcQ'

    @classmethod
    def test_youtube_video_search_exception_is_caught(cls, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeSearch, attribute='__init__', side_effect=Exception('Test exception')):

            response: Response = cls._request_video_search(test_client)
            assert response.status_code == 500

    @classmethod
    def test_search_results_are_returned(cls, test_client: TestClient) -> None:

        response: Response = cls._request_video_search(test_client)
        assert response.status_code == 200
        json_response: list[dict[str, str]] = response.json()
        assert type(json_response) is list
        assert len(json_response) > 0
        video_ids: list[str] = [result.get('id') for result in json_response]
        assert any([video_id == cls._result_video_id for video_id in video_ids])
        thumbnail_responses: list[Response] = [requests.get(result.get('thumbnailUrl')) for result in json_response]
        assert all([thumbnail_response.status_code == 200 for thumbnail_response in thumbnail_responses])

    @classmethod
    def _request_video_search(cls, test_client: TestClient) -> Response:

        return test_client.get(cls._end_point)
