import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters import UserAdapter
from ..dtos import UserInput
from ..exceptions import UsernameAlreadyRegisteredException
from ..persistence import UsersPersistence
from ..persistence.domain import DatabaseUser


class UserRegistrationHandler:

    _log: Logger = logging.getLogger(__name__)
    _user_adapter: UserAdapter
    _users_persistence: UsersPersistence

    @inject
    def __init__(
        self,
        user_adapter: UserAdapter = Provide['user_adapter'],
        users_persistence: UsersPersistence = Provide['users_persistence']
    ):

        self._user_adapter = user_adapter
        self._users_persistence = users_persistence

    def register_user(self, user_input: UserInput) -> None:

        self._log.debug(f'Start [funcName](user_input={user_input})')

        database_user: DatabaseUser | None = self._users_persistence.get_user(user_input.username)

        if database_user is None:

            database_user: DatabaseUser = self._user_adapter.adapt_to_persistence(user_input)
            self._users_persistence.add_user(database_user)

        else:

            raise UsernameAlreadyRegisteredException(user_input.username)

        self._log.debug(f'End [funcName](user_input={user_input})')
