import pytest


@pytest.fixture(scope='session')
def test_wrong_password_authentication_credentials() -> dict:

    authentication_credentials = {
        'username': 'test_username',
        'password': 'test_wrong_password'
    }

    return authentication_credentials
