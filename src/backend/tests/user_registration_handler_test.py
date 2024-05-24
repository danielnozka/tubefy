import pytest
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.order(0)
class UserRegistrationHandlerTest:

    _end_point: str = '/api/auth/register'

    @classmethod
    @pytest.mark.dependency(name='user_registration')
    def test_user_is_registered(cls, test_client: TestClient, user_credentials: dict[str, str]) -> None:

        response: Response = cls._request_user_registration(test_client=test_client, user_credentials=user_credentials)
        assert response.status_code == 200

    @classmethod
    @pytest.mark.dependency(depends=['user_registration'], scope='session')
    def test_registering_with_the_same_username_raises_exception(
        cls,
        test_client: TestClient,
        user_credentials: dict[str, str]
    ) -> None:

        response: Response = cls._request_user_registration(test_client=test_client, user_credentials=user_credentials)
        assert response.status_code == 409

    @classmethod
    def _request_user_registration(cls, test_client: TestClient, user_credentials: dict[str, str]) -> Response:

        return test_client.post(url=cls._end_point, data=user_credentials)
