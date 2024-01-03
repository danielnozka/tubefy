import pytest

from fastapi.testclient import TestClient
from httpx import Response
from string import Template
from uuid import UUID, uuid4


@pytest.mark.order(3)
class AudioRecordingGetterTest:

    _get_all_end_point: str = '/api/audio'
    _get_end_point: Template = Template('/api/audio/${audio_recording_id}')
    _expected_audio_recording: dict[str, str | int] = {
        'videoId': 'dQw4w9WgXcQ',
        'title': 'Never gonna give you up',
        'artist': 'Rick Astley',
        'codec': 'mp3',
        'bitRate': 320
    }

    def test_user_authorization_is_required_to_get_all_audio_recordings(self, test_client: TestClient) -> None:

        response = self._request_all_audio_recordings_without_authorization(test_client)
        assert response.status_code == 401

    @pytest.mark.dependency(depends=['audio_recording_addition'], scope='session')
    def test_all_audio_recordings_are_returned(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response = self._request_all_audio_recordings(json_web_token=json_web_token, test_client=test_client)
        assert response.status_code == 200
        json_response = response.json()
        assert type(json_response) == list
        assert len(json_response) > 0
        audio_recording = json_response[0]
        assert audio_recording.get('id') == str(audio_recording_id)

        for attribute, expected_value in self._expected_audio_recording.items():

            assert audio_recording.get(attribute) == expected_value

    def test_user_authorization_is_required_to_get_an_audio_recording(
        self,
        audio_recording_id: UUID,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording_without_authorization(
            audio_recording_id=audio_recording_id,
            test_client=test_client
        )
        assert response.status_code == 401

    @pytest.mark.dependency(depends=['audio_recording_addition'], scope='session')
    def test_audio_recording_is_returned(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording(
            audio_recording_id=audio_recording_id,
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 200

    def test_requesting_a_non_existent_audio_recording_raises_exception(
        self,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording(
            audio_recording_id=uuid4(),
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 404

    def _request_all_audio_recordings_without_authorization(self, test_client: TestClient) -> Response:

        return test_client.get(self._get_all_end_point)

    def _request_all_audio_recordings(self, json_web_token: str, test_client: TestClient) -> Response:

        return test_client.get(self._get_all_end_point, headers={'Authorization': f'Bearer {json_web_token}'})

    def _request_audio_recording_without_authorization(
        self,
        audio_recording_id: UUID,
        test_client: TestClient
    ) -> Response:

        return test_client.get(self._get_end_point.substitute(audio_recording_id=audio_recording_id))

    def _request_audio_recording(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> Response:

        return test_client.get(
            self._get_end_point.substitute(audio_recording_id=audio_recording_id),
            headers={
                'Authorization': f'Bearer {json_web_token}'
            }
        )
