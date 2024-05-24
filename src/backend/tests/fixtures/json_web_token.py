import pytest
from dependency_injector.wiring import inject, Provide
from tubefy.services.json_web_token_handler import JsonWebTokenHandler


@pytest.fixture(scope='session')
@inject
def json_web_token(
    user_credentials: dict[str, str],
    json_web_token_handler: JsonWebTokenHandler = Provide['json_web_token_handler']
) -> str:

    return json_web_token_handler.get_token(user_credentials['username'])
