from fastapi.testclient import TestClient
from httpx import Response
from unittest import mock
from yt_dlp import YoutubeDL


class AudioSampleGetterTest:

    _video_id: str = 'dQw4w9WgXcQ'
    _end_point: str = f'/api/videos/{_video_id}/audio/sample'

    @classmethod
    def test_youtube_download_exception_is_caught(cls, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeDL, attribute='download', side_effect=Exception('Test exception')):

            response: Response = cls._request_audio_sample(test_client)
            assert response.status_code == 500

    @classmethod
    def test_audio_sample_is_returned(cls, test_client: TestClient) -> None:

        response: Response = cls._request_audio_sample(test_client)
        assert response.status_code == 200

    @classmethod
    def test_downloaded_audio_sample_has_been_added(cls, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeDL, attribute='download', side_effect=Exception('Test exception')):

            response: Response = cls._request_audio_sample(test_client)
            assert response.status_code == 200

    @classmethod
    def _request_audio_sample(cls, test_client: TestClient) -> Response:

        return test_client.get(cls._end_point)
