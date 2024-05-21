import pytest

from fastapi.testclient import TestClient
from httpx import Response
from unittest import mock
from yt_dlp import YoutubeDL


@pytest.mark.order(2)
class AudioRecordingAdderTest:

    _video_id: str = 'dQw4w9WgXcQ'
    _end_point: str = f'/api/videos/{_video_id}/audio'
    _audio_download_options: dict[str, str | int] = {
        'title': 'Never gonna give you up',
        'artist': 'Rick Astley',
        'codec': 'mp3',
        'bitRate': 320
    }

    @classmethod
    def test_user_authorization_is_required(cls, test_client: TestClient) -> None:

        response: Response = test_client.post(url=cls._end_point, json=cls._audio_download_options)
        assert response.status_code == 401

    @classmethod
    def test_youtube_download_exception_is_caught(cls, json_web_token: str, test_client: TestClient) -> None:

        with mock.patch.object(target=YoutubeDL, attribute='download', side_effect=Exception('Test exception')):

            response: Response = cls._request_audio_recording_to_be_added(
                json_web_token=json_web_token,
                test_client=test_client
            )
            assert response.status_code == 500

    @classmethod
    @pytest.mark.dependency(name='audio_recording_addition', depends=['user_registration'], scope='session')
    def test_audio_recording_is_added(cls, json_web_token: str, test_client: TestClient) -> None:

        response: Response = cls._request_audio_recording_to_be_added(
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 200

    @classmethod
    @pytest.mark.dependency(depends=['audio_recording_addition'], scope='session')
    def test_adding_the_same_audio_recording_twice_raises_exception(
        cls,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response: Response = cls._request_audio_recording_to_be_added(
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 409

    @classmethod
    def _request_audio_recording_to_be_added(cls, json_web_token: str, test_client: TestClient) -> Response:

        return test_client.post(
            url=cls._end_point,
            json=cls._audio_download_options,
            headers={
                'Authorization': f'Bearer {json_web_token}'
            }
        )
