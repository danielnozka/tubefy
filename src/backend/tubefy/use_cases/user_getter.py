import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.user_adapter import UserAdapter
from ..domain.user import User
from ..exceptions.user_unauthorized_exception import UserUnauthorizedException
from ..persistence.users_persistence import UsersPersistence
from ..persistence.domain.database_user import DatabaseUser
from ..services.json_web_token_handler import JsonWebTokenHandler


class UserGetter:

    _log: Logger = logging.getLogger(__name__)
    _user_adapter: UserAdapter
    _users_persistence: UsersPersistence
    _json_web_token_handler: JsonWebTokenHandler

    @inject
    def __init__(
        self,
        user_adapter: UserAdapter = Provide['user_adapter'],
        users_persistence: UsersPersistence = Provide['users_persistence'],
        json_web_token_handler: JsonWebTokenHandler = Provide['json_web_token_handler']
    ):

        self._user_adapter = user_adapter
        self._users_persistence = users_persistence
        self._json_web_token_handler = json_web_token_handler

    def get(self, token: str) -> User:

        self._log.debug('Start [funcName]()')
        username: str = self._json_web_token_handler.get_username(token)
        database_user: DatabaseUser | None = self._users_persistence.get_user(username)

        if database_user is None:

            raise UserUnauthorizedException('User not found')

        result: User = self._user_adapter.adapt_to_domain(database_user)
        self._log.debug('End [funcName]()')

        return result
