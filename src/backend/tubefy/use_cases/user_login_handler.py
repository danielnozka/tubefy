import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.token_adapter import TokenAdapter
from ..dtos.token_output import TokenOutput
from ..dtos.user_input import UserInput
from ..exceptions.user_unauthorized_exception import UserUnauthorizedException
from ..persistence.users_persistence import UsersPersistence
from ..persistence.domain.database_user import DatabaseUser
from ..services.json_web_token_handler import JsonWebTokenHandler
from ..services.password_hash_handler import PasswordHashHandler


class UserLoginHandler:

    _log: Logger = logging.getLogger(__name__)
    _token_adapter: TokenAdapter
    _users_persistence: UsersPersistence
    _json_web_token_handler: JsonWebTokenHandler
    _password_hash_handler: PasswordHashHandler

    @inject
    def __init__(
        self,
        token_adapter: TokenAdapter = Provide['token_adapter'],
        users_persistence: UsersPersistence = Provide['users_persistence'],
        json_web_token_handler: JsonWebTokenHandler = Provide['json_web_token_handler'],
        password_hash_handler: PasswordHashHandler = Provide['password_hash_handler']
    ):

        self._token_adapter = token_adapter
        self._users_persistence = users_persistence
        self._json_web_token_handler = json_web_token_handler
        self._password_hash_handler = password_hash_handler

    def log_in_user(self, user_input: UserInput) -> TokenOutput:

        self._log.debug(f'Start [funcName](user_input={user_input})')
        database_user: DatabaseUser | None = self._users_persistence.get_user(user_input.username)

        if database_user is not None:

            if self._password_hash_handler.verify_password(user_input.password, database_user.password) is True:

                token: str = self._json_web_token_handler.get_token(database_user.username)
                result: TokenOutput = self._token_adapter.adapt(token)
                self._log.debug(f'End [funcName](user_input={user_input})')

                return result

        raise UserUnauthorizedException('Incorrect username or password')
