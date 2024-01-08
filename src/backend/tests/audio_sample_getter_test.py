from fastapi.testclient import TestClient
from httpx import Response
from unittest import mock
from yt_dlp import YoutubeDL


class AudioSampleGetterTest:

    _video_id: str = 'dQw4w9WgXcQ'
    _end_point: str = f'/api/videos/{_video_id}/audio/sample'

    def test_youtube_download_exception_is_caught(self, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeDL, attribute='download', side_effect=Exception('Test exception')):

            response: Response = self._request_audio_sample(test_client)
            assert response.status_code == 500

    def test_audio_sample_is_returned(self, test_client: TestClient) -> None:

        response: Response = self._request_audio_sample(test_client)
        assert response.status_code == 200

    def test_downloaded_audio_sample_has_been_added(self, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeDL, attribute='download', side_effect=Exception('Test exception')):

            response: Response = self._request_audio_sample(test_client)
            assert response.status_code == 200

    def _request_audio_sample(self, test_client: TestClient) -> Response:

        return test_client.get(self._end_point)
