import pytest

from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.order(0)
class UserRegistrationHandlerTest:

    _end_point: str = '/api/auth/register'

    @pytest.mark.dependency(name='user_registration')
    def test_user_is_registered(self, test_client: TestClient, user_credentials: dict[str, str]) -> None:

        response: Response = self._request_user_registration(test_client=test_client, user_credentials=user_credentials)
        assert response.status_code == 200

    @pytest.mark.dependency(depends=['user_registration'], scope='session')
    def test_registering_with_the_same_username_raises_exception(
        self,
        test_client: TestClient,
        user_credentials: dict[str, str]
    ) -> None:

        response: Response = self._request_user_registration(test_client=test_client, user_credentials=user_credentials)
        assert response.status_code == 409

    def _request_user_registration(self, test_client: TestClient, user_credentials: dict[str, str]) -> Response:

        return test_client.post(url=self._end_point, data=user_credentials)
