import pytest

from fastapi.testclient import TestClient
from httpx import Response
from string import Template
from uuid import UUID


@pytest.mark.order(4)
class AudioRecordingDeleterTest:

    _end_point: Template = Template('/api/audio/${audio_recording_id}')
    _get_all_end_point: str = '/api/audio'

    def test_user_authorization_is_required_to_delete_audio_recording(
        self,
        audio_recording_id: UUID,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording_deletion_without_authorization(
            audio_recording_id=audio_recording_id,
            test_client=test_client
        )
        assert response.status_code == 401

    @pytest.mark.dependency(name='audio_recording_deletion', depends=['audio_recording_addition'], scope='session')
    def test_audio_recording_is_deleted(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording_deletion(
            audio_recording_id=audio_recording_id,
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['audio_recording_deletion'], scope='session')
    def test_deleting_the_same_audio_recording_twice_raises_exception(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> None:

        response = self._request_audio_recording_deletion(
            audio_recording_id=audio_recording_id,
            json_web_token=json_web_token,
            test_client=test_client
        )
        assert response.status_code == 404

    @pytest.mark.dependency(depends=['audio_recording_deletion'], scope='session')
    def test_no_audio_recordings_are_returned(self, json_web_token: str, test_client: TestClient) -> None:

        response = self._request_all_audio_recordings(json_web_token=json_web_token, test_client=test_client)
        assert response.status_code == 200
        json_response = response.json()
        assert type(json_response) == list
        assert len(json_response) == 0

    def _request_audio_recording_deletion_without_authorization(
        self,
        audio_recording_id: UUID,
        test_client: TestClient
    ) -> Response:

        return test_client.delete(self._end_point.substitute(audio_recording_id=audio_recording_id))

    def _request_audio_recording_deletion(
        self,
        audio_recording_id: UUID,
        json_web_token: str,
        test_client: TestClient
    ) -> Response:

        return test_client.delete(
            self._end_point.substitute(audio_recording_id=audio_recording_id),
            headers={
                'Authorization': f'Bearer {json_web_token}'
            }
        )

    def _request_all_audio_recordings(self, json_web_token: str, test_client: TestClient) -> Response:

        return test_client.get(self._get_all_end_point, headers={'Authorization': f'Bearer {json_web_token}'})
