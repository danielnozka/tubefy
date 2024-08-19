import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from ..adapters.token_adapter import TokenAdapter
from ..dtos.token_dto import TokenOutput
from ..dtos.user_credentials_dto import UserInput
from ..exceptions.unauthorized_user_exception import UserUnauthorizedException
from ..persistence.users_persistence import UsersPersistence
from ..persistence.domain.user_persistence_domain import UserPersistenceDomain
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
    ) -> None:

        self._token_adapter = token_adapter
        self._users_persistence = users_persistence
        self._json_web_token_handler = json_web_token_handler
        self._password_hash_handler = password_hash_handler

    async def log_in_user(self, user_input: UserInput) -> TokenOutput:

        self._log.debug(f'Start [funcName](user_input={user_input})')
        user_persistence_domain: UserPersistenceDomain | None = (
            await self._users_persistence.get_user(user_input.username)
        )

        if user_persistence_domain is not None:

            if self._password_hash_handler.verify_password(
                password=user_input.password,
                hashed_password=user_persistence_domain.password
            ) is True:

                token: str = self._json_web_token_handler.get_token(user_persistence_domain.username)
                result: TokenOutput = self._token_adapter.adapt(token)
                self._log.debug(f'End [funcName](user_input={user_input})')

                return result

        raise UserUnauthorizedException('Incorrect username or password')
