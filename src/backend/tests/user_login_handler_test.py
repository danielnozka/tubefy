import pytest

from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.dependency(depends=['user_registration'], scope='session')
@pytest.mark.order(1)
class UserLoginHandlerTest:

    _end_point: str = '/api/auth/login'

    def test_logging_in_with_the_wrong_username_raises_exception(
        self,
        user_credentials: dict[str, str],
        test_client: TestClient
    ) -> None:

        response = self._request_login(test_client, username='wrong_username', password=user_credentials['password'])
        assert response.status_code == 401

    def test_logging_in_with_the_wrong_password_raises_exception(
        self,
        user_credentials: dict[str, str],
        test_client: TestClient
    ) -> None:

        response = self._request_login(test_client, username=user_credentials['username'], password='wrong_password')
        assert response.status_code == 401

    def test_registered_user_is_logged_in(self, user_credentials: dict[str, str], test_client: TestClient) -> None:

        response = self._request_login(
            test_client,
            username=user_credentials['username'],
            password=user_credentials['password']
        )
        assert response.status_code == 200

    def _request_login(self, test_client: TestClient, username: str, password: str) -> Response:

        return test_client.post(
            self._end_point,
            data={
                'username': username,
                'password': password
            }
        )
