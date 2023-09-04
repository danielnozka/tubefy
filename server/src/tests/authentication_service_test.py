import logging
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response

from tubefy.configuration.app_settings import AppSettings


logging.getLogger('urllib3').propagate = False


class AuthenticationServiceTest:

    _register_end_point: str = '/register'
    _login_end_point: str = '/login'

    @classmethod
    def test_user_is_registered(cls, test_authentication_credentials: dict) -> None:

        response = cls._request_register(test_authentication_credentials)

        assert response.status_code == 200

    @classmethod
    def test_registering_the_same_user_twice_raises_exception(cls, test_authentication_credentials: dict) -> None:

        response = cls._request_register(test_authentication_credentials)

        assert response.status_code == 409

    @classmethod
    def test_user_is_logged_in(cls, test_authentication_credentials: dict) -> None:

        response = cls._request_login(test_authentication_credentials)

        assert response.status_code == 200

    @classmethod
    def test_logging_in_with_wrong_username_raises_exception(cls,
                                                             test_wrong_username_authentication_credentials:
                                                             dict) -> None:

        response = cls._request_login(test_wrong_username_authentication_credentials)

        assert response.status_code == 401

    @classmethod
    def test_logging_in_with_wrong_password_raises_exception(cls,
                                                             test_wrong_password_authentication_credentials:
                                                             dict) -> None:

        response = cls._request_login(test_wrong_password_authentication_credentials)

        assert response.status_code == 401

    @classmethod
    @inject
    def _request_register(cls, authentication_credentials: dict,
                          app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = f'http://localhost:{app_settings.server_settings.port}' + cls._register_end_point
        response = requests.post(url, json=authentication_credentials)

        return response

    @classmethod
    @inject
    def _request_login(cls, authentication_credentials: dict,
                       app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = f'http://localhost:{app_settings.server_settings.port}' + cls._login_end_point
        response = requests.post(url, json=authentication_credentials)

        return response
