import pytest


@pytest.fixture(scope='session')
def user_credentials() -> dict[str, str]:

    return {
        'username': 'test_username',
        'password': 'test_password'
    }
