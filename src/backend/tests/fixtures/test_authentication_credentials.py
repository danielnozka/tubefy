import pytest


@pytest.fixture(scope='session')
def test_authentication_credentials() -> dict:

    authentication_credentials = {
        'username': 'test_username',
        'password': 'test_password'
    }

    return authentication_credentials
