import pytest


@pytest.fixture(scope='session')
def test_wrong_username_authentication_credentials() -> dict:

    authentication_credentials = {
        'username': 'test_wrong_username',
        'password': 'test_password'
    }

    return authentication_credentials
